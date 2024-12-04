import psutil
import time
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

io = 0

class SystemMonitor:
    def __init__(self):
        self.sent_bytes = 0
        self.received_bytes = 0

    def update_info(self):
        global io
        # Update system performance information
        cpu_percent = psutil.cpu_percent(interval=1)
        memory_percent = psutil.virtual_memory().percent
        disk_percent = psutil.disk_usage("/").percent

        # Calculate network usage
        net_io = psutil.net_io_counters()
        sent_bytes_diff = net_io.bytes_sent - self.sent_bytes
        received_bytes_diff = net_io.bytes_recv - self.received_bytes
        self.sent_bytes = net_io.bytes_sent
        self.received_bytes = net_io.bytes_recv

        # Print system information
        print("CPU Usage:", f"{cpu_percent:.2f}%")
        print("Memory Usage:", f"{memory_percent:.2f}%")
        print("Disk Usage:", f"{disk_percent:.2f}%")
        print("Network:", f"S: {sent_bytes_diff / 1024:.2f} R: {received_bytes_diff / 1024:.2f} Kbps")

        # Save data to file and send email 
        self.save_data_to_file()
        if io == 0:
            self.send_mail()
            io += 1

    def save_data_to_file(self):
        # Save system performance data to a text file
        cpu_percent = psutil.cpu_percent(interval=1)
        memory_percent = psutil.virtual_memory().percent
        disk_percent = psutil.disk_usage("/").percent
        sent_bytes = self.sent_bytes
        received_bytes = self.received_bytes

        data = (
            f"CPU Usage: {cpu_percent}%\nMemory Usage: {memory_percent}%\nDisk Usage: {disk_percent}%\n"
            f"Sent Bytes: {sent_bytes} bytes\nReceived Bytes: {received_bytes} bytes"
        )
        with open("system_data.txt", "w") as file:
            file.write(data)

    def send_mail(self):
        # Send an email with the system performance data as an attachment
        port = 587  # For starttls
        smtp_server = "smtp-mail.outlook.com"
        sender_email = "ugcsit@hotmail.com"
        receiver_email = "moaz.eid@ejust.edu.eg"
        password = "moaz1234560"
        filename = "system_data.txt"
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = "PC Workload"
        message.attach(MIMEText("PC Workload File Attached Below ↓↓", "plain"))
        with open(filename, "rb") as file:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )
        message.attach(part)
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls(context=context)
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())

    def monitor_system(self):
        while True:
            self.update_info()
            time.sleep(10)  # Update every 10 seconds

def main():
    monitor = SystemMonitor()
    monitor.monitor_system()

if __name__ == "__main__":
    main()
