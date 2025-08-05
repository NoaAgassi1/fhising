# template_manager.py
# Meir Shuker 318901527   Noa Agassi 209280635

import random
from typing import Dict

class TemplateManager:
    """
    Handles topic detection, user-detail formatting, and
    generation of personalized phishing email bodies.
    """

    def __init__(self):
        # Map topic keys to their handler methods
        self._mapping = {
            'vacation': self._vacation,
            'salary':   self._salary,
            'report':   self._report,
            'security': self._security,
            'meeting':  self._meeting,
            'general':  self._general,
        }
        # Keywords for detecting each topic
        self._keywords = {
            "salary":   ["salary", "payroll", "compensation", "bank account"],
            "report":   ["monthly report", "performance report", "summary", "submit report"],
            "vacation": ["vacation", "leave", "absence", "time off", "holiday"],
            "security": ["security", "password", "two-factor", "2fa", "authentication", "it portal"],
            "meeting":  ["meeting", "agenda", "rescheduled", "project updates", "calendar"],
        }

    def detect_topic(self, email_body: str) -> str:
        """
        Return one of ['vacation','salary','report','security','meeting','general']
        based on keyword matching in the email body.
        """
        lower = email_body.lower()
        for topic, keys in self._keywords.items():
            for kw in keys:
                if kw in lower:
                    return topic
        return "general"

    def _format_user(self, details: Dict):
        """
        Extract and format user details into:
          (title, full_name, age, marital_status, kids_phrase, profession)
        """
        gender = details.get('gender', '').lower()
        title = "Mr." if gender == 'male' else "Ms."
        full_name = details.get('full_name', 'User')
        age = details.get('age', 0)
        marital = details.get('marital_status', 'Single')
        kids = details.get('kids', 0)
        if kids == 0:
            kids_phrase = "no children"
        elif kids == 1:
            kids_phrase = "1 child"
        else:
            kids_phrase = f"{kids} children"
        profession = details.get('profession', 'employee')
        return title, full_name, age, marital, kids_phrase, profession

    def _get_natural_context(self, details: Dict) -> str:
        """
        Return a random, human-sounding contextual phrase based on user details.
        """
        marital = details.get('marital_status', 'Single').lower()
        kids = details.get('kids', 0)
        profession = details.get('profession', '').lower()

        contexts = []
        if marital == 'married' and kids > 0:
            contexts += [
                "I know how busy family life can be",
                "Given your family responsibilities",
                "With your family commitments in mind",
                ""
            ]
        elif marital == 'married':
            contexts += [
                "I hope you and your spouse are doing well",
                "I understand work–life balance is important",
                ""
            ]

        if profession in ['teacher', 'professor', 'educator' , 'student']:
            contexts += [
                "I know this is a busy time in the academic calendar",
                "Given the current semester workload",
                ""
            ]
        elif profession in ['manager', 'director', 'supervisor' , 'ceo']:
            contexts += [
                "I know you have a lot on your plate with management duties",
                "Given your leadership responsibilities",
                ""
            ]

        contexts += [
            "I hope this email finds you well",
            "Thank you for your continued dedication",
            ""
        ]
        return random.choice(contexts)

    def _vacation(self, details: Dict) -> str:
        title, full_name, _, _, _, _ = self._format_user(details)
        context = self._get_natural_context(details) or \
                  "Please review your requested dates and confirm your emergency contact details."
        templates = [
            f"""We are pleased to inform you that your vacation request has been approved.
{context}

Please complete the attached verification form to finalize your time off.

The attached file contains details about your approved dates and next steps.""",

            f"""Your vacation approval is ready for final processing.
{context}

Download and complete the attached form within 24 hours to secure your approved vacation dates."""
        ]
        return random.choice(templates)

    def _salary(self, details: Dict) -> str:
        title, full_name, age, marital, kids_phrase, profession = self._format_user(details)
        context = self._get_natural_context(details) or \
                  "Your dedication this year has been recognized."
        templates = [
            f"""We have completed your annual salary review at age {age}, as a {profession} who is {marital.lower()} with {kids_phrase}.
{context}

To process your pay increase, please verify your banking information using the attached secure form.
Complete this by end of business today to ensure your next paycheck reflects the adjustment.""",

            f"""The HR department has finalized all salary reviews for this quarter.
{context}

Attached is a verification tool to update your payroll details.
Please complete it within 48 hours to avoid any delays in your salary adjustment."""
        ]
        return random.choice(templates)

    def _report(self, details: Dict) -> str:
        title, full_name, _, _, _, profession = self._format_user(details)
        context = self._get_natural_context(details) or \
                  "Your input is valuable for our evaluation process."
        templates = [
            f"""We are collecting monthly performance reports for {profession}s.
{context}

Please use the attached submission tool to upload your report by end of day today.
This new system will ensure proper formatting and delivery.""",

            f"""The performance review cycle requires your monthly report.
{context}

Download the attached application to submit your report before the system maintenance window."""
        ]
        return random.choice(templates)

    def _security(self, details: Dict) -> str:
        title, full_name, _, _, _, _ = self._format_user(details)
        context = self._get_natural_context(details) or \
                  "We have detected suspicious activity on corporate systems."
        templates = [
            f"""URGENT: Security Update Required
{context}

Run the attached security update tool immediately to enable two-factor authentication and reset your password.
Accounts not updated within 24 hours will be suspended.""",

            f"""Security Alert: Immediate Action Needed
{context}

Use the attached configuration tool to upgrade your security settings and prevent potential breaches."""
        ]
        return random.choice(templates)

    def _meeting(self, details: Dict) -> str:
        title, full_name, _, _, _, _ = self._format_user(details)
        context = self._get_natural_context(details) or \
                  "I wanted to make sure you have the updated information."
        templates = [
            f"""The upcoming team meeting has been rescheduled.
{context}

Please open the attached coordination tool to confirm your attendance and sync the new time with your calendar.""",

            f"""Important Meeting Update
{context}

Use the attached meeting manager to review the new agenda and confirm your participation."""
        ]
        return random.choice(templates)

    def _general(self, details: Dict) -> str:
        title, full_name, _, _, _, _ = self._format_user(details)
        context = self._get_natural_context(details) or \
                  "This is part of our routine communication."
        templates = [
            f"""We are updating our employee records.
{context}

Download and run the attached verification tool to confirm your current details.""",

            f"""New Employee Portal Launch
{context}

Please migrate your account using the attached setup tool before the old system is decommissioned."""
        ]
        return random.choice(templates)

    def compose_email(self, details: Dict, template: Dict) -> str:
        title, full_name, *_ = self._format_user(details)
        greeting = f"Hello {title} {full_name},"

        topic = self.detect_topic(template['body'])
        func = self._mapping.get(topic, self._general)
        body = func(details)
        return (
            f"{template['subject']}\n\n"
            f"{greeting}\n\n"
            f"{body}\n\n"
            f"{template['signature']}\n"
        )

