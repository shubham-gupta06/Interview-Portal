from django.db import models

class student(models.Model):
	Firstname = models.CharField(max_length=100, null=False)
	LastName  = models.CharField(max_length=100)
	Emailid  = models.EmailField(max_length=250,primary_key=True)

class interview(models.Model):
	title        = models.CharField(max_length=250, null=False)
	start_time   = models.DateTimeField()
	end_time     = models.DateTimeField()

class engaged_students(models.Model):
	student = models.ForeignKey(student, on_delete=models.CASCADE)
	interview = models.ForeignKey(interview, on_delete=models.CASCADE)
