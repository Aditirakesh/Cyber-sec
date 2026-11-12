# Cyber-sec: Web Server Security Assignment

**Indian Institute of Information Technology Allahabad**  
**Department of Information Technology**  
**Course:** Cyber Security (IT-30001) | Autumn Semester 2026  
**Instructor:** Dr. Soumyadev Maity

---

## **1. Project Overview**

This repository contains our group's submission for the **Web Server Security Assignment: Exploitation and Mitigation of Four Vulnerability Categories**.

The objective of this assignment is to demonstrate the exploitation of common web application vulnerabilities and implement appropriate security measures to prevent them.

Our project covers the following four vulnerability categories:

- **SQL Injection (SQLi)**
- **OS Command Injection**
- **Cross-Site Scripting (XSS)**
- **Cross-Site Request Forgery (CSRF)**

Each group member is responsible for implementing one specific vulnerability variant in a shared Flask web application. For each variant, we demonstrate the vulnerable implementation, execute a working exploit, explain its root cause, and implement one mitigation to prevent the attack.

The application is intentionally vulnerable for educational and demonstration purposes. It is designed to run **locally on localhost only** and must never be deployed on a public server.

---

## **2. Team Members and Ownership (Table 3)**

The following table identifies the individual contributions and ownership of each vulnerability variant.

| Member | Roll Number | Vulnerability Category | Variant Implemented |
|---|---|---|---|
| Aditi (M1) | IIT2024007 | SQL Injection | Authentication Bypass |
| Srujan Gawande (M2) | IIT2024016 | Cross-Site Scripting (XSS) | Stored XSS |
| Disha Gupta (M3) | IIT2024039 | OS Command Injection | In-band Injection |
| Apurva (M4) | IIT2024034 | Cross-Site Scripting (XSS) | Reflected XSS |
| Pratishtha (M5) | IIT2024040 | Cross-Site Request Forgery (CSRF) | POST-based Forged Action |

Each member independently develops and demonstrates their assigned variant. No two members implement the same variant.

---

## **3. Technologies Used**

| Component | Technology |
|---|---|
| Backend | Python, Flask |
| Frontend | HTML, CSS |
| Database | SQLite |
| Version Control | Git and GitHub |
| Testing | Browser and HTTP requests |

---

## **4. Application Setup and Execution**

Follow these steps to run the application locally.

**Step 1: Clone the repository**

```bash
git clone https://github.com/Aditirakesh/Cyber-sec.git
cd Cyber-sec
```

**Step 2: Create a virtual environment**

```bash
python3 -m venv venv
```

**Step 3: Activate the virtual environment**

Linux / macOS:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

**Step 4: Install dependencies**

```bash
pip install -r requirements.txt
```

**Step 5: Start the application**

```bash
python app.py
```

**Step 6: Open the application**

Visit the following address in your browser:

`http://127.0.0.1:5000`

The home page provides access to the individual vulnerability modules. Each module contains its vulnerable and secured implementations along with relevant demonstrations.

---

## **5. Application Architecture and Project Structure**

The application uses a modular architecture in which each member's implementation is maintained independently.

- **app.py:** Main application entry point. Automatically discovers and registers the available Flask blueprints from the `modules/` directory.
- **db.py:** Provides database helper functions and manages separate SQLite databases for individual modules.
- **templates/base.html:** Shared base template containing the common application layout and styling.
- **modules/:** Contains the individual vulnerability implementations.
- **templates/:** Contains the HTML templates associated with each module.
- **docs/:** Contains the technical documentation for each vulnerability variant.

### **Repository Structure**

```text
Cyber-sec/
│
├── app.py
├── db.py
├── requirements.txt
│
├── modules/
│   ├── sqli.py
│   ├── xss_stored.py
│   ├── cmdi.py
│   ├── xss_reflected.py
│   └── csrf.py
│
├── templates/
│   ├── base.html
│   ├── sqli/
│   ├── xss_stored/
│   ├── cmdi/
│   ├── xss_reflected/
│   └── csrf/
│
├── data/                 (created automatically on first run, not committed)
│   ├── sqli.db
│   ├── xss_stored.db
│   └── ...
│
├── docs/
│   ├── sqli.md
│   ├── xss_stored.md
│   ├── cmdi.md
│   ├── xss_reflected.md
│   └── csrf.md
│
└── README.md
```

### **Module Responsibilities**

| Module | Member | Functionality |
|---|---|---|
| `sqli.py` | M1 | SQL injection through authentication bypass |
| `xss_stored.py` | M2 | Stored Cross-Site Scripting |
| `cmdi.py` | M3 | In-band OS command injection |
| `xss_reflected.py` | M4 | Reflected Cross-Site Scripting |
| `csrf.py` | M5 | POST-based Cross-Site Request Forgery |

Each module maintains two separate routes:

- **Vulnerable Route (`/vuln/...`):** Contains the intentionally vulnerable implementation and allows demonstration of the assigned exploit.
- **Fixed Route (`/fixed/...`):** Implements the same functionality with an appropriate security mitigation.

This structure allows the same attack payload to be tested against both implementations, demonstrating the effectiveness of the mitigation.

---

## **6. Exploitation and Mitigation Requirements**

Each vulnerability module demonstrates the following five aspects as required by the assignment:

1. **Vulnerable Implementation:** Identification and explanation of the code containing the security flaw.
2. **Working Exploit:** Demonstration of the exact payload or request used to exploit the vulnerability.
3. **Root Cause:** Explanation of why the vulnerability exists and how the attack succeeds.
4. **Implemented Mitigation:** Implementation of one security measure, followed by testing the same payload to show that the attack is blocked.
5. **Other Mitigation Techniques (Theory):** Explanation of alternative security measures discussed in the course lectures.

The alternative mitigation techniques are documented theoretically and do not require separate implementation.

---

## **7. Documentation**

Each member maintains an individual technical write-up under the `docs/` directory.

Every write-up includes:

- Description of the assigned vulnerability and variant.
- Vulnerable code and explanation.
- Exploit payload and observed output.
- Root cause of the vulnerability.
- Implemented mitigation and its working.
- Evidence showing the attack being blocked.
- Explanation of alternative mitigation techniques discussed in class.

---

## **8. Video Demonstration**

As part of the submission, the group will prepare a screen-recorded video demonstration with voice-over.

Each member will individually demonstrate their assigned vulnerability, including:

- The vulnerable implementation.
- The working exploit and its output.
- The root cause of the vulnerability.
- The implemented security mitigation.
- The same payload being blocked after applying the mitigation.

Each member will narrate their own section to clearly establish individual contributions.

The expected duration is approximately **2–3 minutes per member**.

---

## **9. GitHub Collaboration and Contribution Guidelines**

To maintain independent development and avoid conflicts, each member works on their assigned module.

- Each member develops their implementation in their own module file.
- Associated HTML templates are maintained in separate folders.
- Individual documentation is maintained in the `docs/` directory.
- Members work on separate Git branches.
- Completed changes are submitted through Pull Requests into the `main` branch.

The following files are shared across the project:

- `app.py`
- `db.py`
- `templates/base.html`
- `requirements.txt`

Changes to shared files should be discussed with the group before implementation to avoid integration conflicts.

---

## **10. Submission Deliverables**

The final submission includes:

1. **GitHub Repository:** Complete source code of the application in a public repository.
2. **Video Demonstration:** Group screen recording with individual voice-over demonstrations of all assigned vulnerability variants and their mitigations.
3. **Ownership Declaration:** Completed Table 3 mapping each member to their assigned vulnerability and variant.
4. **Technical Documentation:** Individual write-ups covering exploitation, root cause, implemented mitigation, and alternative mitigation techniques.
5. **Viva:** Individual demonstration and explanation of each member's implementation.

---

## **11. Security Disclaimer**

This project is developed strictly for academic and educational purposes as part of the Cyber Security course at IIIT Allahabad.

The vulnerable implementations are intentionally designed to demonstrate common web application security flaws. All testing and exploitation must be restricted to our own locally hosted application.

**Do not deploy the intentionally vulnerable application on public servers or test it against external systems.**