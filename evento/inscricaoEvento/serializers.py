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

class PessoaSerializer(serializers.HyperlinkedModelSerializer):
	usuario = UserSerializer(many=False)
	class Meta:
		model = Pessoa
		fields = ('usuario','nome', 'sexo', 'idade')

class EventoSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Evento
		fields = '__all__'

class TicketSerializer(serializers.HyperlinkedModelSerializer):
	evento = EventoSerializer(many=False)
	class Meta:
		model = Ticket
		fields = '__all__'

class InscricaoSerializer(serializers.HyperlinkedModelSerializer):
	participante = PessoaSerializer(many=False)
	tickets = TicketSerializer(many=True)
	evento = EventoSerializer(many=False)
	class Meta:
		model = Inscricao
		fields = '__all__'
