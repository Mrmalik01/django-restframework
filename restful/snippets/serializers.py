from rest_framework import serializers
from .models import Snippet, LANGUAGE_CHOICES, STYLES_CHOICES
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    # Primary key based linking
    # snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())

    # Hyperlinked based linking
    snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'snippets']

class SnippetSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField('snippet-highlight', format='html')

    class Meta:
        model = Snippet
        fields = ['url', 'id', 'owner', 'highlight', 'title', 'code', 'linenos', 'language', 'style']

class SnippetSerializer_2(serializers.Serializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    code = serializers.CharField(style={'base_template' : "textarea.html"})
    linenos = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    style = serializers.ChoiceField(choices=STYLES_CHOICES, default='friendly')

    def create(self, validated_data):
        """
        :param validated_data:
        :return: Query Set object of the Snippet model

        Create and return a new 'Snippet' instance, given teh validated data
        """
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        :param instance:
        :param validated_data:
        :return: Query Set object of the Snippet model

        Update and return an existing 'Snippet' instance, given the validated data
        """

        instance.title = validated_data.get("title", instance.title)
        instance.code = validated_data.get("code", instance.code)
        instance.linenos = validated_data.get("linenos", instance.linenos)
        instance.language = validated_data.get("language", instance.language)
        instance.style = validated_data.get("style", instance.style)
        instance.save()
        return instance

