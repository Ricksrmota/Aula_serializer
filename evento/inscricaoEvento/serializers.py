from rest_framework import routers, serializers, viewsets
from django.contrib.auth.models import User
from inscricaoEvento.models import Pessoa
from inscricaoEvento.models import Evento
from inscricaoEvento.models import Ticket
from inscricaoEvento.models import Inscricao

class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = User
		fields = ('url', 'username', 'email')
	def create(self, validated_data):
		user = User.objects.create(**validated_data)
		return user

class PessoaSerializer(serializers.HyperlinkedModelSerializer):
	usuario = UserSerializer(many=False)
	class Meta:
		model = Pessoa
		fields = ('usuario','nome', 'sexo', 'idade')
	def create(self, dados):
		pessoa_data = dados.pop('usuario') #remove o relacionamento de usuario com a pessoa
		u = User.objects.create(**pessoa_data) #cria o objeto de usuario separadamente
		p = Pessoa.objects.create(usuario=u, **dados) #a tag de usuario tem que ser a mesma do models, aqui cria a pessoa e passa ambos!
		return p

class EventoSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Evento
		fields = '__all__'
	def create(self, dados):
		event = Evento.objects.create(**dados)
		return event

class TicketSerializer(serializers.HyperlinkedModelSerializer):	
	evento = EventoSerializer(many=False)
	class Meta:
		model = Ticket
		fields = '__all__'
	def create(self, dados):		
		evento_data = dados.pop('evento')
		e = Evento.objects.create(**evento_data)
		t = Ticket.objects.create(evento = e, **dados)
		return t
class InscricaoSerializer(serializers.HyperlinkedModelSerializer):
	participante = PessoaSerializer(many=False)
	tickets = TicketSerializer(many=False)
	evento = EventoSerializer(many=False)
	class Meta:
		model = Inscricao
		fields = '__all__'
	def create(self, dados):
		participante_data = dados.pop('participante')
		tickets_data = dados.pop('tickets')
		evento_data = dados.pop('evento')
		e = Evento.objects.create(**evento_data)
		t = Ticket.objects.create(evento = e, **dados)
		p = Pessoa.objects.create(**participante_data)
		i = Inscricao.objects.create(participante = p, Ticket = t, **dados)
		return i

