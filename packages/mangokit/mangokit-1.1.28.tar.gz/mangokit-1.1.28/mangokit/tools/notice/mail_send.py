# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 邮箱通知封装
# @Time   : 2022-11-04 22:05
# @Author : 毛鹏
import smtplib
from email.mime.text import MIMEText
from smtplib import SMTPException
from socket import gaierror

from mangokit.exceptions import SendMessageError, ERROR_MSG_0016, ERROR_MSG_0017
from mangokit.models.models import EmailNoticeModel, TestReportModel


class EmailSend:

    def __init__(self, notice_config: EmailNoticeModel, test_report: TestReportModel = None, domain_name: str = None):
        self.test_report = test_report
        self.notice_config = notice_config
        self.domain_name = domain_name

    def send_main(self) -> None:
        if self.test_report.test_suite_id:
            content = f"""
            各位同事, 大家好:
                测试套ID：{self.test_report.test_suite_id}任务执行完成，执行结果如下:
                用例运行总数: {self.test_report.case_sum} 个
                通过用例个数: {self.test_report.success} 个
                失败用例个数: {self.test_report.fail} 个
                异常用例个数: {self.test_report.warning} 个
                跳过用例个数: 暂不统计 个
                成  功   率: {self.test_report.success_rate} %
    
    
            **********************************
            芒果自动化平台地址：{self.domain_name}
            详细情况可前往芒果自动化平台查看，非相关负责人员可忽略此消息。谢谢！
            """
        else:
            content = f"""
            各位同事, 大家好:
                用例运行总数: {self.test_report.case_sum} 个
                通过用例个数: {self.test_report.success} 个
                失败用例个数: {self.test_report.fail} 个
                异常用例个数: {self.test_report.warning} 个
                跳过用例个数: 暂不统计 个
                成  功   率: {self.test_report.success_rate} %


            **********************************
            芒果自动化平台地址：{self.domain_name}
            详细情况可前往芒果自动化平台查看，非相关负责人员可忽略此消息。谢谢！
            """
        try:
            self.send_mail(self.notice_config.send_list, f'【芒果测试平台通知】', content)
        except SMTPException:
            raise SendMessageError(*ERROR_MSG_0016)

    def send_mail(self, user_list: list, sub: str, content: str, ) -> None:
        try:
            user = f"MangoTestPlatform <{self.notice_config.send_user}>"
            message = MIMEText(content, _subtype='plain', _charset='utf-8')
            message['Subject'] = sub
            message['From'] = user
            message['To'] = ";".join(user_list)
            server = smtplib.SMTP()
            server.connect(self.notice_config.email_host)
            server.login(self.notice_config.send_user, self.notice_config.stamp_key)  # 登录qq邮箱
            server.sendmail(user, user_list, message.as_string())  #
            server.close()
        except gaierror:
            raise SendMessageError(*ERROR_MSG_0017)
