from rest_framework import serializers

from brand.models import Brand


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

    def validate_name(self, value):
        if Brand.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError("Такой бренд уже существует.")
        return value