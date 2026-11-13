"""Reflected Cross-Site Scripting (Reflected XSS) - Module 4
Owner: Apurva (M4)

Routes:
    /xss_reflected/          Hub page linking to vulnerable and fixed search routes
    /xss_reflected/vuln/     Vulnerable version (query reflected without escaping via | safe)
    /xss_reflected/fixed/    Secured version (protected by Jinja2 context-aware auto-escaping)
"""
from flask import Blueprint, render_template, request

OWNER = "Apurva (M4)"
READY = True
TITLE = "Cross-Site Scripting (Reflected XSS)"
bp = Blueprint("xss_reflected", __name__, url_prefix="/xss_reflected")

# Static Academic Dataset for Campus Resource Search
CAMPUS_RESOURCES = [
    {
        "id": 1,
        "title": "Python Programming Master Notes & OOPs Guide",
        "category": "Programming Notes",
        "code": "CS-201",
        "description": "Comprehensive notes covering Python fundamentals, control structures, object-oriented concepts, exception handling, and file I/O with practical code examples.",
        "tags": ["python", "programming", "oops"]
    },
    {
        "id": 2,
        "title": "Data Structures & Algorithms: Trees, Graphs & DP",
        "category": "Data Structures & Algorithms",
        "code": "CS-203",
        "description": "In-depth lecture notes covering binary search trees, AVL trees, Dijkstra's algorithm, BFS/DFS graph traversals, and dynamic programming.",
        "tags": ["dsa", "algorithms", "trees", "graphs"]
    },
    {
        "id": 3,
        "title": "Operating Systems: Process Synchronization & Concurrency",
        "category": "Operating Systems",
        "code": "CS-301",
        "description": "Detailed explanation of critical sections, semaphores, mutex locks, Peterson's algorithm, and classic synchronization problems.",
        "tags": ["operating systems", "os", "concurrency", "semaphores"]
    },
    {
        "id": 4,
        "title": "Operating Systems: Virtual Memory & Paging Algorithms",
        "category": "Operating Systems",
        "code": "CS-301",
        "description": "Illustrated guide to paging, segmentation, TLB operation, page faults, FIFO, LRU, and Optimal page replacement algorithms.",
        "tags": ["operating systems", "os", "paging", "memory"]
    },
    {
        "id": 5,
        "title": "Computer Networks: OSI 7-Layer & TCP/IP Protocol Suite",
        "category": "Computer Networks",
        "code": "CS-305",
        "description": "Complete breakdown of network layer architectures, packet encapsulation, IP addressing, subnetting, and TCP 3-way handshake.",
        "tags": ["computer networks", "networking", "tcp/ip", "osi"]
    },
    {
        "id": 6,
        "title": "Database Management Systems: Relational Algebra & SQL",
        "category": "Database Management Systems",
        "code": "CS-204",
        "description": "Core concepts of the relational model, tuple relational calculus, DDL/DML SQL queries, joins, and view definitions.",
        "tags": ["dbms", "database", "sql", "queries"]
    },
    {
        "id": 7,
        "title": "DBMS: Normalization (1NF to BCNF) & ACID Transactions",
        "category": "Database Management Systems",
        "code": "CS-204",
        "description": "Functional dependencies, canonical cover, lossless decomposition, dependency preservation, 1NF through BCNF, and 2-Phase Locking.",
        "tags": ["dbms", "normalization", "acid", "transactions"]
    },
    {
        "id": 8,
        "title": "Previous Year Question Paper (2024): Data Structures",
        "category": "Previous Year Questions",
        "code": "CS-203",
        "description": "Official end-semester examination question paper (December 2024) including model answers and mark distribution.",
        "tags": ["pyq", "dsa", "exam", "previous year"]
    },
    {
        "id": 9,
        "title": "Previous Year Question Paper (2023): Operating Systems",
        "category": "Previous Year Questions",
        "code": "CS-301",
        "description": "Official end-semester paper covering process scheduling algorithms, deadlock handling, memory virtualization, and Linux commands.",
        "tags": ["pyq", "os", "exam", "previous year"]
    },
    {
        "id": 10,
        "title": "Engineering Semester Exam Quick Revision & Formula Sheet",
        "category": "Study Materials",
        "code": "ALL-CS",
        "description": "High-yield formula cheat sheet summarizing Big-O complexities, tree formulas, network socket states, and SQL aggregate syntax.",
        "tags": ["revision", "cheat sheet", "study materials", "formula"]
    }
]


def setup():
    """No database tables needed for Reflected XSS; using in-memory sample resources."""
    pass


def filter_resources(query_str):
    """Search sample resources matching the query string in title, description, or tags."""
    if not query_str:
        return CAMPUS_RESOURCES

    q_lower = query_str.lower().strip()
    matched = []
    for res in CAMPUS_RESOURCES:
        in_title = q_lower in res["title"].lower()
        in_desc = q_lower in res["description"].lower()
        in_cat = q_lower in res["category"].lower()
        in_tags = any(q_lower in tag.lower() for tag in res["tags"])
        if in_title or in_desc or in_cat or in_tags:
            matched.append(res)
    return matched


@bp.route("/", strict_slashes=False)
def index():
    """Hub page for Reflected XSS module."""
    return render_template("xss_reflected/index.html")


@bp.route("/vuln", methods=["GET"], strict_slashes=False)
def vuln():
    """
    Vulnerable Search Endpoint:
    Receives search query parameter 'q' via GET and reflects it into
    templates/xss_reflected/vuln.html using Jinja2's '| safe' filter.
    Bypassing output escaping allows injected scripts to execute in the browser.
    """
    query = request.args.get("q", "")
    results = filter_resources(query) if query else []
    return render_template(
        "xss_reflected/vuln.html",
        query=query,
        results=results,
        results_count=len(results)
    )


@bp.route("/fixed", methods=["GET"], strict_slashes=False)
def fixed():
    """
    Secured Search Endpoint:
    Receives search query parameter 'q' via GET and reflects it into
    templates/xss_reflected/fixed.html using standard Jinja2 interpolation {{ query }}.
    Jinja2's context-aware auto-escaping encodes HTML entities, neutralizing XSS.
    """
    query = request.args.get("q", "")
    results = filter_resources(query) if query else []
    return render_template(
        "xss_reflected/fixed.html",
        query=query,
        results=results,
        results_count=len(results)
    )
