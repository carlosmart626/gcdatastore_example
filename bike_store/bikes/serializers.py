from rest_framework import serializers
from .datastore import create_update_instance


class BikeSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=200)
    price = serializers.FloatField()
    manufacturer = serializers.CharField()

    def create(self, validated_data):
        self.instance = create_update_instance(validated_data)
        self.id = self.instance.get('id')
        return self.instance

    def update(self, instance, validated_data):
        self.instance = create_update_instance(validated_data, instance.get('id'))
        self.id = self.instance.get('id')
        return self.instance
