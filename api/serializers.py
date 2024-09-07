from rest_framework import serializers

from players.models import Alliance, Player, PlayerStatus


class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Player
        fields = (
            "game_id",
            "nick",
            "rank",
            "specialty",
            "status",
            "observacao",
            "alliance",
            "func",
        )


class AllianceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Alliance
        fields = "__all__"


class PlayerStatusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PlayerStatus
        fields = "__all__"
