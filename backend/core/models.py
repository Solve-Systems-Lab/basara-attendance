"""
The whole data model. Nine tables, one file, about 200 lines.

Read this file end to end before Day 2. You can hold the entire system in
your head, and that is deliberate — you will spend the fortnight adding to it.
"""
import json

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# --------------------------------------------------------------- people

class Student(models.Model):
    """One row per student. Linked to a Django auth user for login.

    We use django.contrib.auth rather than storing passwords ourselves.
    Rolling your own authentication is one of the most reliable ways to
    put a real vulnerability into a real system.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student")
    roll_no = models.CharField(max_length=20, unique=True, db_index=True)
    name = models.CharField(max_length=120)
    branch = models.CharField(max_length=10)
    year = models.PositiveSmallIntegerField(default=4)
    is_active = models.BooleanField(default=True)

    # Day 7. No face processing may happen for a student until this is True.
    # A student may withdraw consent at any time, without giving a reason,
    # and marks attendance by instructor override instead. See spec.md §4.
    consent_given = models.BooleanField(default=False)
    consent_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["roll_no"]

    def __str__(self):
        return f"{self.roll_no} {self.name}"


class Subject(models.Model):
    code = models.CharField(max_length=12, unique=True)
    name = models.CharField(max_length=120)

    class Meta:
        ordering = ["code"]

    def __str__(self):
        return f"{self.code} {self.name}"


# --------------------------------------------------------------- the timetable

class ClassSession(models.Model):
    """One period of one subject on one day. Attendance hangs off this."""
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="sessions")
    date = models.DateField(db_index=True)
    period = models.PositiveSmallIntegerField()  # 1..5
    room = models.CharField(max_length=30, default="LH-1")

    class Meta:
        ordering = ["-date", "period"]
        constraints = [
            models.UniqueConstraint(fields=["date", "period"], name="one_session_per_period"),
        ]

    def __str__(self):
        return f"{self.subject.code} {self.date} P{self.period}"


class Holiday(models.Model):
    date = models.DateField(unique=True)
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ["date"]

    def __str__(self):
        return f"{self.name} ({self.date})"


# --------------------------------------------------------------- attendance

class AttendanceRecord(models.Model):
    """The central table. One row per student per session.

    Note what is stored versus what is trusted. `latitude`, `longitude` and
    `accuracy_m` are recorded for audit but are NEVER used to accept or reject
    a mark — see presence/signals.py and the Day 6 notes. Anything a client
    can set, a client can lie about.
    """
    PRESENT = "PRESENT"
    ABSENT = "ABSENT"
    STATUS_CHOICES = [(PRESENT, "Present"), (ABSENT, "Absent")]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="records")
    session = models.ForeignKey(ClassSession, on_delete=models.CASCADE, related_name="records")
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default=ABSENT)
    marked_at = models.DateTimeField(null=True, blank=True)

    photo = models.ImageField(upload_to="marks/%Y/%m/%d/", null=True, blank=True)

    # Recorded, never trusted.
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    accuracy_m = models.FloatField(null=True, blank=True)

    # Day 7. The cosine similarity that let this mark through.
    face_score = models.FloatField(null=True, blank=True)

    # Which signals actually passed, e.g. {"campus_ip": true, "code": true}
    signals = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-session__date", "student__roll_no"]
        constraints = [
            models.UniqueConstraint(fields=["student", "session"], name="one_record_per_student_session"),
        ]
        indexes = [models.Index(fields=["student", "status"])]

    def __str__(self):
        return f"{self.student.roll_no} {self.session} {self.status}"


# --------------------------------------------------------------- Day 6: presence

class SessionCode(models.Model):
    """The rotating code on the projector.

    Short-lived and single-use per student. Neither property is optional:
    a code with no expiry is a code someone posts in the group chat, and a
    code with no single-use rule is one a friend can redeem for you.
    """
    code = models.CharField(max_length=8, unique=True, db_index=True)
    session = models.ForeignKey(ClassSession, on_delete=models.CASCADE, related_name="codes", null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField()

    class Meta:
        ordering = ["-created_at"]

    def is_live(self):
        return self.created_at <= timezone.now() <= self.expires_at

    def __str__(self):
        return f"{self.code} (expires {self.expires_at:%H:%M:%S})"


class CodeRedemption(models.Model):
    """Enforces 'one student, one use' for a given code."""
    code = models.ForeignKey(SessionCode, on_delete=models.CASCADE, related_name="redemptions")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="redemptions")
    at = models.DateTimeField(default=timezone.now)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["code", "student"], name="one_redemption_per_student"),
        ]


class AuditLog(models.Model):
    """Every attempt to mark attendance — accepted or rejected, with the reason.

    Day 6 lab. When a student disputes their attendance three weeks from now,
    this table is the only thing that will settle it. Log rejections especially:
    a system that only records its successes cannot be audited.
    """
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True)
    at = models.DateTimeField(default=timezone.now, db_index=True)
    action = models.CharField(max_length=40, default="mark")
    accepted = models.BooleanField(default=False)
    reason = models.CharField(max_length=80, blank=True)

    ip = models.GenericIPAddressField(null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    accuracy_m = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ["-at"]

    def __str__(self):
        verdict = "ok" if self.accepted else f"rejected:{self.reason}"
        return f"{self.at:%Y-%m-%d %H:%M} {self.student_id} {verdict}"


# --------------------------------------------------------------- Day 7: faces

class EnrolmentPhoto(models.Model):
    """One of a student's ~10 reference photos, plus its face embedding.

    The embedding is 512 floats stored as JSON text. A binary column would be
    smaller; text is readable, and being able to open the row and see the
    numbers is worth more to you this fortnight than the bytes.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="enrolment")
    image = models.ImageField(upload_to="enrol/%Y/%m/")
    embedding = models.TextField(blank=True)  # JSON list[float], length 512
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["student__roll_no", "id"]

    def vector(self):
        """The embedding as a list of floats, or None if not computed yet."""
        return json.loads(self.embedding) if self.embedding else None

    def set_vector(self, vec):
        self.embedding = json.dumps([round(float(x), 6) for x in vec])

    def __str__(self):
        return f"{self.student.roll_no} enrolment #{self.id}"
