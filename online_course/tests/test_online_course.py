import pytest
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestOnlineCourse(TransactionCase):
    
    def setUp(self):
        super().setUp()
        
        # create test teacher
        self.teacher = self.env['res.users'].create({
            'name': 'Test Teacher',
            'login': 'teacher_test',
            'email': 'teacher@test.com',
        })
        # create test teacher
        self.student = self.env['res.users'].create({
            'name': 'Test Student', 
            'login': 'student_test',
            'email': 'student@test.com',
        })
    
    def test_teacher_not_student_constraint(self):
        """We are testing here, that teacher can not be student and teacher together in one course."""
        course = self.env['online.course'].create({
            'name': 'Test Course',
            'teacher_id': self.teacher.id,
            'student_ids': [(4, self.student.id)],
        })
        
        with pytest.raises(ValidationError):
            course.student_ids = [(4, self.teacher.id)]
    
    def test_negative_price_constraint(self):
        """We are testing here, that negative price is forbidden always."""
        course = self.env['online.course'].create({
            'name': 'Test Course',
            'teacher_id': self.teacher.id,
            'price': -10.0,
        })
        
        with pytest.raises(ValidationError):
            course.state = 'published'
    
    def test_free_course_can_be_published(self):
        """We are testing here, that free courses are able to publish."""
        course = self.env['online.course'].create({
            'name': 'Free Course',
            'teacher_id': self.teacher.id,
            'price': 0.0,
        })
        
        course.state = 'published'
        assert course.state == 'published'
    
    def test_paid_course_can_be_published(self):
        """We are testing here, that paid courses are publishable."""
        course = self.env['online.course'].create({
            'name': 'Paid Course',
            'teacher_id': self.teacher.id,
            'price': 99.99,
        })
        
        course.state = 'published'
        assert course.state == 'published'
    
    def test_course_count_computation(self):
        """We are testing here course counting."""
        # create courses
        self.env['online.course'].create({
            'name': 'Course 1',
            'teacher_id': self.teacher.id,
        })
        self.env['online.course'].create({
            'name': 'Course 2',
            'teacher_id': self.teacher.id,
        })
        
        # recount course_count
        self.teacher._compute_course_count()
        
        assert self.teacher.course_count == 2
    
    def test_course_defaults(self):
        """We are testing here, that if we have created course, then default values are those, which we set in models."""
        course = self.env['online.course'].create({
            'name': 'Default Course',
            'teacher_id': self.teacher.id,
        })
        
        assert course.state == 'draft'
        assert course.price == 0.0
