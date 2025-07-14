# Online Course Management

Simple Odoo module for online courses.

## Features

- **Courses** with teachers and students
- **Course state** (draft/published/archived)
- **Smart button** for teachers with number of courses
- **Colorful kanban** view (wasn't checked because I have black and white screen)
- **Access rules** for user roles

## Installation

1. clone this repository or download it
2. copy folder online_course to somewhere, where odoo expects addons (you can specify it with parameter `--addon-path` when you run ./odoo-bin, ie `./odoo-bin -d your_db --addons-path="./addons,./actin_addons"`)
3. Restart Odoo server
4. Go to Apps and install "Online Course"

## Using

1. **Create course:** Online Courses → Courses → New
2. **Set teachers** and students
3. **Publish course** (the price constrains is set to >= 0)
4. **Views:** Kanban (green=published, gray=draft) [NOT TESTED]

## Testing
If you want to run tests, you need to add PyTest to your virtual environment or to your system (not recommended, but possible).
```bash
pip install pytest
```
Only when you have PyTest installed, you can run tests:
```bash
python odoo-bin -d your_db -i online_course --test-enable
```

## Technical details

- **Models:** `online.course`, `online.course.enrollment`
- **Constraints:** Teacher≠Student, Price≥0 for publishing
- **ACL:** Students are able to see only published courses
- **Computed fields:** course_count for teachers

## Author

Jiri - 2025

## Note:
This module is created for Actin/Vilgain as a showcase.
