FROM python:3.13.3

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN python3 -m pip install -r requirements.txt

# Copy application files
COPY . .

# Set the entry point to run the calculator
ENTRYPOINT ["python", "calculator.py"]