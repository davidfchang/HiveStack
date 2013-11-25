from datetime import datetime, date, timedelta
from django.db import models
from django.contrib.auth.models import User
from django.utils.six import with_metaclass


# HiveStack MVP

class IDType(models.Model):  #CI o Pasaporte
    name = models.CharField(max_length=20, blank=True)


class UserProfile(models.Model): # a user that can be an implementer or a project creator
    user = models.ForeignKey(User, unique=True, related_name='user')
    followers = models.ManyToManyField('self', related_name='followers', symmetrical=False)
    created_date = models.DateTimeField(blank=True, default=datetime.today())
    username = models.CharField(max_length=20, blank=True) #for shortened urls
    first_name = models.CharField(max_length=50, blank=True)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    company_name = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, blank=True)
    phone_number = models.CharField(max_length=50)
    id_type = models.ForeignKey(IDType, unique=True, related_name='ID type')
    id = models.CharField(max_length=50, blank=True, unique=True) #cedula o pasaporte
    ssn = models.CharField(max_length=50, blank=True, unique=True) #for work in the US
    email = models.EmailField()
    birthday = models.DateTimeField(blank=False) # underage users can't work on nsfw projects
    profession = models.CharField(max_length=100, blank=True)
    bio = models.TextField(max_length=500, blank=True) #all action, actions speak louder than words (140 characters)

    def age(self): #returns a number of years
        if self.birthday > date.today().replace(year=self.birthday.year):
            return date.today().year - self.birthday.year - 1
        else:
            return date.today().year - self.birthday.year

    def is_adult(self): #returns if user is an adult
        return self.age(self) >= 18

    twitter_handler = models.CharField(max_length=15, blank=True)
    facebook_profile = models.URLField()
    linkedin_url = models.URLField()
    angelco_url = models.URLField()
    website = models.URLField()
    #picture = models.ImageField()

    def __unicode__(self):
        return self.username


class Project(models.Model): # a project that needs to be built in separate tasks and then merged
    owner = models.ForeignKey(
        UserProfile) #the user profile (project champion/product owner) that leads a project, a user can have several projects pointing to him

    created_date = models.DateTimeField(blank=True, default=datetime.today())
    modified_date = models.DateTimeField(blank=True, default=datetime.today())
    title = models.CharField(max_length=60)
    purpose = models.TextField(max_length=500, blank=True)
    description = models.TextField(max_length=500, blank=False)
    #image = models.ImageField()
    twitter_handler = models.CharField(max_length=15, blank=True)
    facebook_profile = models.URLField()
    linkedin_url = models.URLField()
    angelco_url = models.URLField()
    website = models.URLField()
    # 5 industry tags
    # 5 required skill tags: coder/merger/designer/business...
    # logo = models.ImageField()
    # 5 purpose tags

    def __unicode__(self):
        return self.title


class Task(models.Model): #an essential task that has to be built for a project to work
    requesting_user = models.ForeignKey(UserProfile) #the user that needs it done
    project = models.ForeignKey(Project) #the project a task belongs to
    building_user = models.ForeignKey(UserProfile) #the user that implemented it
    reward_budget = models.DecimalField(max_digits=20, decimal_places=2)
    deadline = models.DateTimeField(blank=True,
                                    default=(datetime.today() + timedelta(days=20))) #date the task is due
    created_date = models.DateTimeField(blank=True, default=datetime.today()) #when was the task created

    title = models.CharField(max_length=60)
    description = models.TextField(max_length=500, blank=True) #what the task is about
    inspiration_url = models.URLField() #link to what the product owner wants as a reference
    is_urgent = models.BooleanField(default=False) #is the task time sensitive?
    is_critical = models.BooleanField(default=False) #is the task critical for the project?
    is_complete = models.BooleanField(default=False) #is the task complete?
    completed_date = models.DateTimeField(blank=True) #when was the task completed?
    # 5 required skill tags
    def __unicode__(self):
        return self.title


class Bid(models.Model): #a bid an implementer can make for a task that needs to be built
    task = models.ForeignKey(Task) #the task this bid
    bidder = models.ForeignKey(UserProfile) #the user that offers to undertake the task
    title = models.CharField(max_length=60)
    description = models.TextField(max_length=500, blank=True) #what the bidder offers to accomplish
    price = models.DecimalField(max_digits=20, decimal_places=2)
    time_span = models.IntegerField() #time in days the bidder offers to deliver finished task
    review = models.TextField(max_length=500, blank=True) #what the project owner thinks of the delivered bid
    attachment_url = models.URLField() #link to dropbox directory where deliverable is hosted
    inspiration_url = models.URLField() #link to what the bidder used as an inspiration
    bidding_date = models.DateTimeField(blank=True, default=datetime.today()) #when was the bid created
    delivered_date = models.DateTimeField(blank=True) #when was the bid delivered

    received_payment = models.BooleanField(default=False) #has the product owner paid the bidder?
    was_accepted = models.BooleanField(default=False) #has the product owner accepted the bid?
    # 5 required skill tags
    def __unicode__(self):
        return self.title


class Review(models.Model): #accumulated quality_karma,  accumulated_manager_karma, reciprocity profile,
    reviewed_user = models.ForeignKey(UserProfile, related_name="reviewed user profiles",
                                      related_query_name="reviewed user profile")
    reviewed_task = models.ForeignKey(Task, related_name="reviewed task", related_query_name="reviewed task")
    title = models.CharField(max_length=60)
    description = models.TextField(max_length=500,
                                   blank=True) #what the product owner thinks of the bidder's deliverable

    #rating values - 1: UNACCEPTABLE, 2:ACCEPTABLE, 3:EXCEEDS EXPECTATIONS
    reciprocity = models.IntegerField() #i feel the bidder got the upper hand, it was a fair_trade, i feel he/she gave much more than what i'm paying for
    usefulness = models.IntegerField() #this is useless, the end result is as i imagined it, i'm awed to this marvel
    compatibility = models.IntegerField() #i don't know how to merge this with my project, i think someone can merge this, i could merge this myself, piece of cake
    happiness = models.IntegerField() #this feels boring, this is in sync with what i wanted, this incredible, it exceeds what i wanted
    haste = models.IntegerField() #he did this slow, he took the time he said he would,  he was lightning fast

    def __unicode__(self):
        return self.title


class Announcement(models.Model):
    posting_user = models.ForeignKey(UserProfile) #the user that needs it done
    posting_date = models.DateTimeField(default=datetime.now()) #when was the bid delivered
    title = models.CharField(max_length=100, blank=False)
    content = models.TextField(max_length=500, blank=True) #announcement text
    attachment_url = models.URLField() #optional link

    project = models.ForeignKey(Project) #the project the announcement is about
    task = models.ForeignKey(Task) #the task the announcement is about
    bid = models.ForeignKey(Bid) #the bid the announcement is about
    review = models.ForeignKey(Review) #the review the announcement is about

    likes = models.IntegerField() #likes
    dislikes = models.IntegerField() #dislikes

    def __unicode__(self):
        return self.title


class Comment(models.Model):
    announcement = models.ForeignKey(Announcement)
    posting_user = models.ForeignKey(UserProfile) #the user that needs it done
    posting_date = models.DateTimeField(default=datetime.now()) #when was the bid delivered
    content = models.TextField(max_length=500, blank=True) #announcement text
    attachment_url = models.URLField() #optional link

    likes = models.IntegerField() #likes
    dislikes = models.IntegerField() #dislikes

    def __unicode__(self):
        return self.content


#class Tag(models.Model):
#    tagged_object = models.ForeignKey(models.Model, related_name="tags", related_query_name="tag")


class IndustryTag(models.Model): # a project can belong to certain industries
    project = models.ForeignKey(Project, related_name="industry tags", related_query_name="industry tag")
    name = models.CharField(max_length=25)


class RequiredSkillTag(models.Model): # a task in project requires certain skills to get it done
    task = models.ForeignKey(Task, related_name="required skill tags", related_query_name="required skill tag")
    name = models.CharField(max_length=25)


class UserSkillTag(models.Model): # a user can have mastery of several skills
    user_profile = models.ForeignKey(UserProfile, related_name="user skill tags", related_query_name="user skill tag")
    name = models.CharField(max_length=25)