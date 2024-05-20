from rest_framework import serializers
from .models import (
    User, Education, Form1A, Course, Form1B, Form2, Form3A, Form3B, Committee, Comment,
    Form3C, Form4A, Form4B, Examiner, Form4C, Form4D, Form4E, Form5, Form6
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']

class TokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()
    user = UserSerializer()  # Include the user serializer here
    
class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'

class Form1ASerializer(serializers.ModelSerializer):
    education = EducationSerializer(many=True, read_only=True)

    class Meta:
        model = Form1A
        fields = '__all__'
        depth = 1

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class Form1BSerializer(serializers.ModelSerializer):
    course = CourseSerializer(many=True, read_only=True)

    class Meta:
        model = Form1B
        fields = '__all__'

class Form2Serializer(serializers.ModelSerializer):
    class Meta:
        model = Form2
        fields = '__all__'

class Form3ASerializer(serializers.ModelSerializer):
    class Meta:
        model = Form3A
        fields = '__all__'

class Form3BSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form3B
        fields = '__all__'

class CommitteeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Committee
        fields = '__all__'

class Form3CSerializer(serializers.ModelSerializer):
    committee = CommitteeSerializer(many=True, read_only=True)

    class Meta:
        model = Form3C
        fields = '__all__'
        depth = 1

class Form4ASerializer(serializers.ModelSerializer):
    committee = CommitteeSerializer(many=True, read_only=True)

    class Meta:
        model = Form4A
        fields = '__all__'
        depth = 1

class Form4BSerializer(serializers.ModelSerializer):
    committee = CommitteeSerializer(many=True, read_only=True)

    class Meta:
        model = Form4B
        fields = '__all__'
        depth = 1

class ExaminerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Examiner
        fields = '__all__'

class Form4CSerializer(serializers.ModelSerializer):
    indian_examiner = ExaminerSerializer(read_only=True)
    foreign_examiner = ExaminerSerializer(read_only=True)
    committee = CommitteeSerializer(many=True, read_only=True)

    class Meta:
        model = Form4C
        fields = '__all__'
        depth = 1

class Form4DSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form4D
        fields = '__all__'

class Form4ESerializer(serializers.ModelSerializer):
    class Meta:
        model = Form4E
        fields = '__all__'

class Form5Serializer(serializers.ModelSerializer):
    class Meta:
        model = Form5
        fields = '__all__'

class CommentSerializer(serializers.Serializer):
    class Meta:
        model = Comment
        fields = '__all__'   

class Form6Serializer(serializers.ModelSerializer):
    comment = serializers.CharField(required=False)
    committee = CommitteeSerializer(many=True, read_only=True)

    class Meta:
        model = Form6
        fields = '__all__'
        depth = 1
