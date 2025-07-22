# eVerify Integration Checklist

## Phase 1: Prepare eVerify Package

### ✅ Step 1.1: Create Standalone Package
```bash
python package_everify.py
```
- Creates `everify_standalone_package/` directory
- Includes all necessary files and resources

### ✅ Step 1.2: Set Environment Variablesl
```bash
# eVerify API credentials
export CLIENT_ID="your_client_id"
export CLIENT_SECRET="your_client_secret"

# PostgreSQL database for this project
export PGHOST="localhost"
export PGPORT="5432"
export PGUSER="postgres"
export PGPASSWORD="your_password"
export PGDATABASE="your_project_verifications"  # Unique per project
```

### ✅ Step 1.3: Create PostgreSQL Database
```sql
-- Create database
CREATE DATABASE your_project_verifications;

-- Connect to database
\c your_project_verifications

-- Create verifications table (for checking already verified users)
CREATE TABLE verifications (
    id SERIAL PRIMARY KEY,
    reference VARCHAR(255),
    code VARCHAR(255),
    first_name VARCHAR(255),
    middle_name VARCHAR(255),
    last_name VARCHAR(255),
    birth_date DATE,
    face_key VARCHAR(255),
    gender VARCHAR(50),
    marital_status VARCHAR(50),
    municipality VARCHAR(255),
    province VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Note:** The `verifications` table is used only to check if a person has already been verified, so they don't need to go through the verification process again. Each application will handle their own specific data needs separately.

### ✅ Step 1.4: Install Dependencies
```bash
cd everify_standalone_package
pip install -r requirements.txt
```

### ✅ Step 1.5: Test eVerify Package
```bash
python launch_everify.py
```

---

## Phase 2: Set Up Flask Server for Face Liveness (REQUIRED)

### ✅ Step 2.1: Start Flask Server
```bash
# Start the Flask server for face liveness functionality
python flask_server/app.py
```
**Note**: The Flask server must be running for face liveness checks to work.

### ✅ Step 2.2: Verify Flask Server is Running
- Open browser and go to: `http://127.0.0.1:5000/liveness`
- You should see the liveness check page
- The server should be accessible on port 5000

### ✅ Step 2.3: Configure Liveness URLs (if needed)
```python
# In everify_standalone.py, verify these URLs are correct:
liveness_url = "http://127.0.0.1:5000/liveness"
liveness_result_url = "http://127.0.0.1:5000/liveness_result"
```

---

## Phase 3: Integrate into Your Desktop App

### ✅ Step 3.1: Add eVerify Button
```python
# In your desktop app
self.everify_button = QPushButton("🔍 Launch eVerify")
self.everify_button.clicked.connect(self.launch_everify)
```

### ✅ Step 3.2: Implement Launch Function
```python
def launch_everify(self):
    """Launch eVerify standalone application."""
    try:
        everify_path = "everify_standalone_package/everify_standalone.py"
        self.everify_process = subprocess.Popen([
            sys.executable, everify_path
        ])
        # Start timer to check for completion
        self.result_timer.start(2000)
    except Exception as e:
        QMessageBox.critical(self, "Error", f"Failed to launch eVerify: {str(e)}")
```

### ✅ Step 3.3: Add Result Checking
```python
def check_everify_result(self):
    """Check if eVerify has completed."""
    if self.everify_process and self.everify_process.poll() is not None:
        # Process finished, check database for results
        self.check_database_for_results()
```

### ✅ Step 3.4: Implement Database Result Checking
```python
def check_database_for_results(self):
    """Check database for recent verification results."""
    # Connect to database and query recent verifications
    # Update UI with results
    # Handle verification data in your app
```

### ✅ Step 3.5: Handle Verification Results
```python
def handle_verification_result(self, full_name, verification_data):
    """Process verification result in your application."""
    # Update your app's database
    # Enable features based on verification
    # Update UI elements
    # Send notifications
    # etc.
```

---

## Phase 4: Testing and Validation

### ✅ Step 4.1: Test Basic Integration
- [ ] Flask server is running on port 5000
- [ ] eVerify button launches standalone app
- [ ] Verification process completes successfully
- [ ] Face liveness check works properly
- [ ] Results appear in database
- [ ] Your app detects and displays results

### ✅ Step 4.2: Test Error Handling
- [ ] Missing credentials handled gracefully
- [ ] Database connection errors handled
- [ ] Network errors handled
- [ ] Flask server not running - proper error message
- [ ] User cancellation handled

### ✅ Step 4.3: Test Different Scenarios
- [ ] Manual verification (personal info + face liveness)
- [ ] QR code verification (with face liveness)
- [ ] Face liveness check completes successfully
- [ ] Already verified person
- [ ] Failed verification
- [ ] Flask server down - proper error handling

---

## Phase 5: Production Deployment

### ✅ Step 5.1: Environment Setup
- [ ] Set production environment variables
- [ ] Configure production PostgreSQL database
- [ ] Set up proper file paths
- [ ] Ensure Flask server starts automatically

### ✅ Step 5.2: Flask Server Deployment
- [ ] Deploy Flask server to production server
- [ ] Configure firewall to allow port 5000
- [ ] Set up SSL/HTTPS for production
- [ ] Configure auto-restart for Flask server

### ✅ Step 5.3: Security
- [ ] Secure credential storage
- [ ] Database access controls
- [ ] Network security for Flask server
- [ ] HTTPS for liveness endpoints

### ✅ Step 5.4: Monitoring
- [ ] Add logging for verification attempts
- [ ] Monitor database performance
- [ ] Track verification success rates
- [ ] Monitor Flask server health

---

## File Structure After Integration

```
your_project/
├── your_desktop_app.py          # Your main application
├── everify_standalone_package/   # eVerify package
│   ├── everify_standalone.py
│   ├── everify/
│   ├── launch_everify.py
│   └── requirements.txt
├── flask_server/                 # REQUIRED: for face liveness
│   ├── app.py
│   ├── static/
│   └── templates/
│       └── liveness.html
└── database/                     # Your project database
    └── verifications table
```

---

## Integration Methods

### Method 1: Simple Launch (Any App)
```python
import subprocess
subprocess.run(["python", "everify_standalone_package/everify_standalone.py"])
```

### Method 2: Advanced Integration (Python Apps)
```python
# Launch and monitor
self.everify_process = subprocess.Popen([...])
# Check database for results
```

### Method 3: VBA Integration
```vba
Shell "python path\to\everify_standalone.py", vbNormalFocus
```

---

## Complete Verification Flow

1. **User clicks eVerify button** in your desktop app
2. **eVerify standalone app launches** with personal info/QR tabs
3. **System checks if user is already verified** (using verifications table)
4. **If already verified**: Shows face image and skips verification
5. **If not verified**: User enters data (manual or QR scan)
6. **Face liveness check starts** (opens browser to Flask server)
7. **User completes face verification** in browser
8. **eVerify app receives liveness session ID**
9. **Final verification** with eVerify API (includes liveness)
10. **Results stored** in verifications table (for future checks)
11. **Your app receives verification result** and handles its own data needs
12. **Your app integrates verification data** into its own database/records

---

## Data Handling and Application Integration

### **eVerify System Data (verifications table):**
- **Purpose**: Check if users are already verified (skip duplicate verifications)
- **Data**: Basic verification info (name, birth date, face image, etc.)
- **Usage**: Only for verification status checking

### **Your Application Data:**
- **Purpose**: Handle your specific business needs
- **Data**: Whatever your application requires (customer info, records, etc.)
- **Usage**: Your application's own database and business logic

### **Integration Example:**
```python
def handle_verification_result(self, full_name, verification_data):
    """Process verification result in your application."""
    
    # 1. Verification is complete - user is confirmed real
    print(f"✅ User verified: {full_name}")
    
    # 2. Now handle your application's specific needs
    if self.is_customer_registration():
        # Store customer data in your customer database
        self.store_customer_data(verification_data)
        
    elif self.is_loan_application():
        # Update loan application with verified identity
        self.update_loan_application(verification_data)
        
    elif self.is_government_service():
        # Process government service application
        self.process_government_service(verification_data)
    
    # 3. Your application continues with its normal workflow
    self.enable_next_step()
```

### **Key Points:**
- **eVerify handles verification** (is this person real?)
- **Your app handles business logic** (what do you need to do with this person?)
- **Separate databases** for different purposes
- **Flexible integration** - each app can use verification data differently

---

## Troubleshooting

### Common Issues:
1. **eVerify not found**: Run `package_everify.py` first
2. **Database connection error**: Check PostgreSQL and environment variables
3. **Authentication error**: Verify CLIENT_ID and CLIENT_SECRET
4. **Face liveness not working**: Ensure Flask server is running on port 5000
5. **Flask server won't start**: Check if port 5000 is available
6. **Browser doesn't open for liveness**: Check firewall/antivirus settings

### Debug Steps:
1. Check environment variables
2. Test database connection
3. Verify eVerify API credentials
4. Ensure Flask server is running: `http://127.0.0.1:5000/liveness`
5. Check file paths and permissions
6. Test face liveness manually in browser 