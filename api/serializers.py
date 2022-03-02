from rest_framework import serializers
from kvk.models import Kvk, Zerado
from mge.models import Inscrito, Mge, Punido, Ranking
from players.models import Alliance, Player, PlayerStatus


# Player module Models


class PlayerSerializerForStaff(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Player
        fields = [
            "game_id",
            "nick",
            "rank",
            "specialty",
            "status",
            "observacao",
            "alliance",
            "alterado_em",
            "__str__",
        ]


class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Player
        fields = [
            "game_id",
            "nick",
            "specialty",
            "status",
            "alliance",
            "__str__",
        ]


class AllianceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Alliance
        fields = ["nome", "tag", "__str__"]


class PlayerStatusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PlayerStatus
        fields = [
            "player",
            "data",
            "power",
            "killpoints",
            "deaths",
            "editavel",
            "revisavel",
            "__str__",
        ]


# MGE module models


class MgeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Mge
        fields = ["criado_em", "tipo", "semana", "__str__"]


class PunidoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Punido
        fields = ["player", "mge", "inserido"]


class RankingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ranking
        fields = ["player", "mge", "inserido"]


class InscritoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Inscrito
        fields = ["player", "mge", "kills", "deaths", "general", "inserido"]


# Kvk module models


class KvkSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Kvk
        fields = ["inicio", "final", "tipo", "ativo", "__str__"]


class ZeradoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Zerado
        fields = ["kvk", "player", "date"]
