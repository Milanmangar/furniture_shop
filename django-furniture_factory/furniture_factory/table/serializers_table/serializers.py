from django.db.models import Q
from rest_framework import serializers
from table.models import Table, Leg


class TableSerializer(serializers.ModelSerializer):
    description = serializers.CharField()
    price = serializers.IntegerField()
    legs = serializers.PrimaryKeyRelatedField(read_only=False, queryset=Leg.objects.all())

    class Meta:
        fields = ["name", "legs", "description", "price", "created_date", "last_updated_date"]
        model = Table

    def validate(self, data):
        request_method = self.context["request"]._request.method
        if request_method.lower() == "post":
            is_valid_leg = Leg.objects.filter(name__iexact=data["legs"].name).exists()
            leg_exists = Table.objects.filter(legs=data["legs"].name).exists()
            if not is_valid_leg or leg_exists:
                all_legs_in_table = [table.legs.name for table in Table.objects.all()]
                available_legs = [leg.name for leg in Leg.objects.filter(~Q(name__in=all_legs_in_table))]
                if available_legs:
                    raise serializers.ValidationError("'{}' is invalid legs, valid legs options are {}".
                                                      format(data["legs"], available_legs))
                else:
                    raise serializers.ValidationError("No 'Legs' available, Please request 'Admin' to create new 'legs'")
        return data
