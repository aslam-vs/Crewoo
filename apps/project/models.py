from django.db import models
from apps.core.validators import validate_file_extension
from apps.staffs.models import *
from .managers import *


class BaseClass(models.Model):

    """
        Base class for all models
    """
    createdon = models.DateTimeField(auto_now_add=True)
    lastmodon = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class ProjectBase(BaseClass):
    title = models.CharField(max_length=30, null=False, blank=False)
    short_description = models.CharField(
        max_length=300, null=False, blank=False)
    detailed_description = models.TextField(null=False, blank=False)
    start_date = models.DateTimeField(null=False, blank=False)
    end_date = models.DateTimeField(null=False, blank=False)

    class Meta:
        abstract = True


class Project(ProjectBase):
    manager = models.ForeignKey(Staff, null=False, blank=False)
    client_name = models.CharField(max_length=30, null=False, blank=False)
    attachments = models.ManyToManyField('ProjectAttachment')
    createdby = models.ForeignKey(Staff, related_name='project_createdby')
    modifiedby = models.ForeignKey(Staff, related_name='project_modifedby')
    objects = ProjectManager()

    class Meta:
        verbose_name = ('Project')
        verbose_name_plural = ('Projects')

    def __unicode__(self):
        return self.client_name


class ProjectAttachment(BaseClass):
    file = models.FileField(upload_to="project/attachment",
                            validators=[validate_file_extension], max_length=200, blank=True)

    # def __unicode__(self):
    #     return self.title


class Modules(BaseClass):
    project = models.ForeignKey(Project, null=False, blank=False)
    title = models.CharField(max_length=30, null=False, blank=False)
    short_description = models.CharField(
        max_length=300, null=False, blank=False)
    detailed_description = models.TextField(null=False, blank=False)
    createdby = models.ForeignKey(Staff, related_name='modules_createdby')
    modifiedby = models.ForeignKey(Staff, related_name='modules_modifedby')

    class Meta:
        verbose_name = ('Module')
        verbose_name_plural = ('Modules')

    def __unicode__(self):
        return self.title


class Tasks(BaseClass):
    modules = models.ForeignKey(Modules, null=False, blank=False)
    title = models.CharField(max_length=30, null=False, blank=False)
    short_description = models.CharField(
        max_length=300, null=False, blank=False)
    detailed_description = models.TextField(null=False, blank=False)
    createdby = models.ForeignKey(Staff, related_name='task_createdby')
    modifiedby = models.ForeignKey(Staff, related_name='task_modifedby')

    class Meta:
        verbose_name = ('Task')
        verbose_name_plural = ('Tasks')

    def __unicode__(self):
        return self.title


class Comments(models.Model):
    project = models.ForeignKey(
        Project, related_name='comments', null=False, blank=False)
    subject = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=False, blank=False)
