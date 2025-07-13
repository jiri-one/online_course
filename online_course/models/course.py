from odoo import fields, api
from odoo.exceptions import ValidationError
from odoo.models import Model


class OnlineCourse(Model):
    _name = "online.course"
    _description = "Online Course"

    name = fields.Char(required=True)
    description = fields.Text()
    price = fields.Float(default=0.0)
    teacher_id = fields.Many2one("res.users", string="Teacher", required=True)
    student_ids = fields.Many2many("res.users", string="Students")
    state = fields.Selection(
        [("draft", "Draft"), ("published", "Published"), ("archived", "Archived")],
        default="draft",
        required=True,
    )

    @api.constrains("teacher_id", "student_ids")
    def _check_teacher_not_student(self):
        """User can not be student and teacher together in one course."""
        for course in self:
            if course.teacher_id in course.student_ids:
                raise ValidationError(
                    f"Učitel '{course.teacher_id.name}' nemůže být současně studentem kurzu '{course.name}'."
                )

    @api.constrains("state", "price")
    def _check_publish_price(self):
        """Paid course can be published only if price is >= 0."""
        for course in self:
            if course.state == "published":
                if course.price >= 0:
                    # Free courses can be published always
                    # and paid courses can be published it their price is higher then 0
                    continue
                elif course.price < 0:
                    raise ValidationError(
                        f"Kurz '{course.name}' nelze publikovat se zápornou cenou."
                    )


class OnlineCourseEnrollment(Model):
    _name = "online.course.enrollment"
    _description = "Course Enrollment"

    course_id = fields.Many2one("online.course", string="Course", required=True)
    student_id = fields.Many2one("res.users", string="Student", required=True)
    enroll_date = fields.Date(default=fields.Date.today)
    status = fields.Selection(
        [
            ("enrolled", "Enrolled"),
            ("completed", "Completed"),
            ("dropped", "Dropped"),
            ("suspended", "Suspended"),
        ],
        default="enrolled",
        required=True,
    )  # this is only ideas, not sure if it is needed
