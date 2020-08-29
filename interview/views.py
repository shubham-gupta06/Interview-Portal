from django.shortcuts import render, redirect
from datetime import datetime
from .models import *
from django.contrib import messages

def home(request):
	students = student.objects.all()
	return render(request,'interview/home.html', {'students': students})
def check_overlap(d1_input, d2_input, d3_data, d4_data):
	d1_input = d1_input.replace(tzinfo=None)
	d2_input = d2_input.replace(tzinfo=None)
	d3_data = d3_data.replace(tzinfo=None)
	d4_data = d4_data.replace(tzinfo=None)
	if(d1_input>=d3_data and d1_input<d4_data):
		return False
	if(d2_input>d3_data and d2_input<=d4_data):
		return False
	return True


def create_interview(request):
	if request.method == "POST":
		students_object = student.objects.all()
		students = request.POST.getlist('student')
		if len(students) < 2:
			messages.error(request, 'Enter atleast 2 participants for interview.')
			return redirect('home-view')
		start_times = request.POST.get('start-time')
		end_times = request.POST.get('end-time')
		title = request.POST.get('title')
		start_date, start_time = start_times.split('T')
		sy, sm, sd = list(map(int, start_date.split('-')))
		shr,smin =list(map(int,start_time.split(':')))

		end_date, end_time = end_times.split('T')
		ey, em, ed = list(map(int, end_date.split('-')))
		ehr,emin = list(map(int,end_time.split(':')))
		start_value=datetime(sy,sm,sd,shr,smin)
		end_value=datetime(ey,em,ed,ehr,emin)
		if(start_value>=end_value):
			messages.error(request, 'Please enter valid dates.')
			return redirect('home-view')

		not_available = []
		for email in students:
 			engaged_students_data = engaged_students.objects.filter(student__Emailid=email)
 			for data in engaged_students_data:
 				interview_obj = data.interview
 				obj = interview.objects.get(pk=interview_obj.id)

 				sdate = obj.start_time
 				edate = obj.end_time
 				if not check_overlap(start_value, end_value, sdate, edate):
 					not_available.append(email)
		not_available = list(set(not_available))
		if len(not_available) > 0:
 			msg_string = ", ".join(not_available)
 			msg_string = "These students are no longer available: " + msg_string
 			messages.error(request, msg_string)
 			return redirect('home-view')
		interview_object = interview(title=title, start_time=start_value, end_time=end_value)
		interview_object.save()
		print(interview_object.id)
		for stu in students:
 			student_from_database = student.objects.get(pk=stu)
 			interview_from_database = interview.objects.get(pk=interview_object.id)
 			engaged_object = engaged_students(student=student_from_database, interview= interview_from_database)
 			engaged_object.save()
		messages.success(request, "Interview successfully scheduled")
		return redirect('home-view')

def scheduled(request):
	interviews = interview.objects.all()
	interview_students_details = {}
	for intv in interviews:
		engaged_obj = engaged_students.objects.filter(interview=intv)
		l = []
		for obj in engaged_obj:
			l.append(obj.student)
		interview_students_details[intv] = l

	return render(request,'interview/scheduled.html', {'interview_students_details': interview_students_details})

def edit(request):
	if request.method == "GET":
		id = int(request.GET.get('interview-id'))
		interview_obj = interview.objects.get(pk=id)

		engaged_objects = engaged_students.objects.filter(interview=interview_obj)
		students_list = []

		for obj in engaged_objects:
			students_list.append(obj.student.Emailid)

		students_list = set(students_list)

		all_students = student.objects.all()

		temp_dict = {}

		for stu in all_students:
			if stu.Emailid in students_list:
				temp_dict[stu] = True
			else:
				temp_dict[stu] = False
		return render(request,'interview/edit.html', {'student_dict': temp_dict, 'interview': interview_obj})

	else:
		students_object = student.objects.all()
		students = request.POST.getlist('student')
		if len(students) < 2:
			messages.error(request, 'Enter atleast 2 participants for interview.')
			return redirect('home-view')
		start_times = request.POST.get('start-time')
		end_times = request.POST.get('end-time')
		title = request.POST.get('title')
		start_date, start_time = start_times.split('T')
		sy, sm, sd = list(map(int, start_date.split('-')))
		shr,smin =list(map(int,start_time.split(':')))

		end_date, end_time = end_times.split('T')
		ey, em, ed = list(map(int, end_date.split('-')))
		ehr,emin = list(map(int,end_time.split(':')))
		start_value=datetime(sy,sm,sd,shr,smin)
		end_value=datetime(ey,em,ed,ehr,emin)
		if(start_value>=end_value):
			messages.error(request, 'Please enter valid dates.')
			return redirect('home-view')

		not_available = []
		for email in students:
 			engaged_students_data = engaged_students.objects.filter(student__Emailid=email)
 			for data in engaged_students_data:
 				interview_obj = data.interview
 				obj = interview.objects.get(pk=interview_obj.id)

 				sdate = obj.start_time
 				edate = obj.end_time
 				if not check_overlap(start_value, end_value, sdate, edate):
 					not_available.append(email)
		not_available = list(set(not_available))
		if len(not_available) > 0:
 			msg_string = ", ".join(not_available)
 			msg_string = "These students are no longer available: " + msg_string
 			messages.error(request, msg_string)
 			return redirect('home-view')


		id = int(request.POST.get('interview-id'))
		interview_obj = interview.objects.get(pk=id)

		interview_obj.title = title
		interview_obj.end_time = end_value
		interview_obj.start_time = start_value
		interview_obj.save()

		print(interview_obj.id)
		interview_from_database = interview.objects.get(pk=interview_obj.id)


		engaged_students.objects.filter(interview=interview_from_database).delete()

		for stu in students:
 			student_from_database = student.objects.get(pk=stu)
 			engaged_object = engaged_students(student=student_from_database, interview= interview_from_database)
 			engaged_object.save()
		messages.success(request, "Interview successfully edited")
		return redirect('home-view')

