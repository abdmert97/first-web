from django.db import models
from django.contrib.auth.models import User
# SuperUserInformation
# User: Jose
# Email: training@pieriandata.com
# Password: testpassword


AEE = 'AEE'
CE = 'CE'
CENG = 'CENG'
OTHERS = 'OTHERS'
dept_choices = (
    (None, '#--Please select the department!--#'),
    (AEE, 'Aerospace Engineering'),
    (CE, 'Civil Engineering'),
    (CENG, 'Computer Engineering'),
    (OTHERS, 'Other departments'),
)


class UserInfo(models.Model):

    # Create relationship (don't inherit from User!)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='usr')

    def __str__(self):
        # Built-in attribute of django.contrib.auth.models.User !
        return self.user.username


class Team(models.Model):
    name = models.CharField(max_length=200, unique=True)
    admin_usr = models.OneToOneField(UserInfo, on_delete=models.CASCADE, unique=True, null=True, related_name='Team')
    base_dept = models.CharField(max_length=4, choices = dept_choices[:-1])
    def __str__(self):
        return self.name    
             

class Player(models.Model):
    name = models.CharField(max_length=200)
    dept = models.CharField(max_length = 6, choices = dept_choices)
    student_id = models.CharField(max_length=7, unique=True, blank=False, default="0000000")
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_members', null=True, blank = False)

    def __str__(self):
        return self.name

