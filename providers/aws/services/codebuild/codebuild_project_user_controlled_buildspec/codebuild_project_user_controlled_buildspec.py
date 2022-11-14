from re import search

from lib.check.models import Check, Check_Report
from providers.aws.services.codebuild.codebuild_client import codebuild_client


class codebuild_project_user_controlled_buildspec(Check):
    def execute(self):
        findings = []
        for project in codebuild_client.projects:
            report = Check_Report(self.metadata)
            report.region = project.region
            report.resource_id = project.name
            report.resource_arn = ""
            report.status = "FAIL"
            report.status_extended = f"CodeBuild project {project.name} does not use a user controlled buildspec"
            if project.buildspec:
                if search(".*\.yaml$", project.buildspec) or search(
                    ".*\.yml$", project.buildspec
                ):
                    report.status = "PASS"
                    report.status_extended = f"CodeBuild project {project.name} uses a user controlled buildspec"

            findings.append(report)

        return findings