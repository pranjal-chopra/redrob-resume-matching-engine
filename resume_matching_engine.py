import math


# ─────────────────────────────────────────────────────────────
# 0.  RAW DATA
# ─────────────────────────────────────────────────────────────

RESUMES = {
    "Arjun Sharma":    "Pyhton, MachineLearning, SQL, pandas, numpy, Deep-learning",
    "Priya Nair":      "JavaScrpit, Reacts, Node.JS, MongoDb, REST api, HTML/CSS",
    "Rahul Gupta":     "Java, Spring Boot, MySql, Microservices, Docker, kubernates",
    "Sneha Patel":     "Python, TensorFlow, Keras, NLP, BERT, data-viz, matplotlib",
    "Vikram Singh":    "C++, Algoritms, Data Structure, competitive programming, python",
    "Ananya Krishnan": "javascript, vue.js, python, flask, PostgreSQL, AWS, CI/CD",
    "Karan Mehta":     "Python, Sklearn, XGboost, feature engineering, SQL, tableau",
    "Deepika Rao":     "Java, Android, Kotlin, Firebase, REST, UI/UX, figma",
    "Aditya Kumar":    "Reactjs, TypeScrpit, GraphQL, redux, tailwind, nodejs, jest",
    "Meera Iyer":      "python, R, statistics, ML, regression, clustering, Power-BI",
}

JDS = {
    "JD1": {
        "label":     "JD-1 — Kakao (ML Engineer)",
        "required":  "Python, Machine Learning, Deep Learning, TensorFlow, PyTorch, SQL, Data Visualization",
        "preferred": "NLP, BERT, Feature Engineering, Statistics",
    },
    "JD2": {
        "label":     "JD-2 — Naver (Backend Engineer)",
        "required":  "Java, Spring Boot, MySQL, PostgreSQL, Microservices, Docker, Kubernetes",
        "preferred": "REST API, CI/CD, Redis",
    },
    "JD3": {
        "label":     "JD-3 — Line (Frontend Engineer)",
        "required":  "JavaScript, React, Vue, TypeScript, REST API, HTML/CSS",
        "preferred": "Node.js, GraphQL, Redux, Jest, AWS",
    },
}

# ─────────────────────────────────────────────────────────────
# 1.  SKILL ALIASES  (used exactly as provided — not modified)
# ─────────────────────────────────────────────────────────────

SKILL_ALIASES = {
    # Languages
    "python": "python",
    "pyhton": "python",
    "java": "java",
    "javascript": "javascript",
    "javascrpit": "javascript",
    "js": "javascript",
    "typescript": "typescript",
    "typescrpit": "typescript",
    "c++": "cpp",
    "cpp": "cpp",
    "r": "r",
    "kotlin": "kotlin",
    # ML / Data
    "machinelearning": "machine_learning",
    "machine learning": "machine_learning",
    "ml": "machine_learning",
    "sklearn": "machine_learning",
    "deeplearning": "deep_learning",
    "deep learning": "deep_learning",
    "deep-learning": "deep_learning",
    "tensorflow": "tensorflow",
    "pytorch": "pytorch",
    "keras": "keras",
    "nlp": "nlp",
    "bert": "bert",
    "xgboost": "xgboost",
    "feature engineering": "feature_engineering",
    "statistics": "statistics",
    "stats": "statistics",
    "regression": "regression",
    "clustering": "clustering",
    "data-viz": "data_visualization",
    "data visualization": "data_visualization",
    "data viz": "data_visualization",
    "matplotlib": "data_visualization",
    "tableau": "data_visualization",
    "power-bi": "data_visualization",
    "power bi": "data_visualization",
    "powerbi": "data_visualization",
    "pandas": "pandas",
    "numpy": "numpy",
    # Web — Frontend
    "react": "react",
    "reacts": "react",
    "reactjs": "react",
    "vue": "vue",
    "vue.js": "vue",
    "vuejs": "vue",
    "redux": "redux",
    "tailwind": "tailwind",
    "html/css": "html_css",
    "html css": "html_css",
    "html": "html_css",
    "css": "html_css",
    "jest": "jest",
    "graphql": "graphql",
    # Web — Backend
    "node.js": "nodejs",
    "nodejs": "nodejs",
    "node js": "nodejs",
    "flask": "flask",
    "spring boot": "spring_boot",
    "springboot": "spring_boot",
    "rest api": "rest_api",
    "rest": "rest_api",
    "restapi": "rest_api",
    "microservices": "microservices",
    # Databases
    "sql": "sql",
    "mysql": "mysql",
    "mysq": "mysql",
    "postgresql": "postgresql",
    "postgres": "postgresql",
    "mongodb": "mongodb",
    "redis": "redis",
    # DevOps / Cloud
    "docker": "docker",
    "kubernetes": "kubernetes",
    "kubernates": "kubernetes",
    "k8s": "kubernetes",
    "ci/cd": "ci_cd",
    "cicd": "ci_cd",
    "ci cd": "ci_cd",
    "aws": "aws",
    # Mobile
    "android": "android",
    "firebase": "firebase",
    # CS Fundamentals
    "algorithms": "algorithms",
    "algoritms": "algorithms",
    "data structure": "data_structures",
    "data structures": "data_structures",
    "competitive programming": "competitive_programming",
    # Design
    "ui/ux": "ui_ux",
    "ui ux": "ui_ux",
    "figma": "figma",
}

# Pre-sort multi-word phrase keys (longest first) so they are
# matched before any single-token key that shares words.
_MULTI_WORD_KEYS = sorted(
    [k for k in SKILL_ALIASES if " " in k],
    key=lambda k: -len(k)
)


# ─────────────────────────────────────────────────────────────
# 2.  STEP 1 + 2 — NORMALIZE & DEDUPLICATE
# ─────────────────────────────────────────────────────────────

def normalize_skills(raw: str) -> list:
    """
    Split on commas → lowercase → alias-map (multi-word first) → deduplicate.
    Tokens absent from SKILL_ALIASES are silently discarded.
    """
    tokens = [t.strip().lower() for t in raw.split(",")]

    canonical = []
    for token in tokens:
        mapped = SKILL_ALIASES.get(token)          # direct lookup (covers multi-word too,
                                                    # since each comma-entry IS one token)
        if mapped:
            canonical.append(mapped)

    # Deduplicate — preserve first-seen order
    seen = set()
    result = []
    for skill in canonical:
        if skill not in seen:
            seen.add(skill)
            result.append(skill)
    return result


# ─────────────────────────────────────────────────────────────
# 3.  STEP 3 — BUILD SHARED VOCABULARY
# ─────────────────────────────────────────────────────────────

def build_vocabulary(normalized_resumes: dict) -> list:
    """Collect every canonical skill from all resumes; sort alphabetically."""
    all_skills = set()
    for skills in normalized_resumes.values():
        all_skills.update(skills)
    return sorted(all_skills)


# ─────────────────────────────────────────────────────────────
# 4.  STEP 4 — TF-IDF VECTORS  (standard math only)
# ─────────────────────────────────────────────────────────────

def compute_tfidf_vectors(normalized_resumes: dict, vocab: list) -> dict:
    """
    TF  = 1 / N          (N = unique skill count after dedup)
    IDF = ln(10 / df)    (df = resumes containing skill; no smoothing)
    TF-IDF = TF * IDF
    """
    N_DOCS = 10

    # Document-frequency per vocab term
    df = {skill: 0 for skill in vocab}
    for skills in normalized_resumes.values():
        for skill in skills:
            df[skill] += 1

    tfidf_vectors = {}
    for name, skills in normalized_resumes.items():
        N = len(skills)
        vec = []
        for skill in vocab:
            if skill in skills:
                tf    = 1.0 / N
                idf   = math.log(N_DOCS / df[skill])
                vec.append(tf * idf)
            else:
                vec.append(0.0)
        tfidf_vectors[name] = vec

    return tfidf_vectors


# ─────────────────────────────────────────────────────────────
# 5.  STEP 5 — JD BINARY VECTORS
# ─────────────────────────────────────────────────────────────

def build_jd_vector(jd_info: dict, vocab: list) -> list:
    """
    Combine required + preferred JD skills, normalize them,
    then produce a binary vector over the shared vocabulary.
    """
    combined  = jd_info["required"] + ", " + jd_info["preferred"]
    jd_skills = set(normalize_skills(combined))
    return [1 if skill in jd_skills else 0 for skill in vocab]


# ─────────────────────────────────────────────────────────────
# 6.  STEP 6 — COSINE SIMILARITY & RANKING
# ─────────────────────────────────────────────────────────────

def cosine_similarity(a: list, b: list) -> float:
    """Cosine(A, B) = dot(A,B) / (|A| * |B|)"""
    dot    = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return dot / (norm_a * norm_b)


def rank_candidates(tfidf_vectors: dict, jd_vec: list) -> list:
    """Return list of (name, score) sorted by score desc, then name asc."""
    scores = [
        (name, cosine_similarity(resume_vec, jd_vec))
        for name, resume_vec in tfidf_vectors.items()
    ]
    scores.sort(key=lambda x: (-x[1], x[0]))
    return scores


# ─────────────────────────────────────────────────────────────
# 7.  MAIN — ORCHESTRATE ALL STAGES
# ─────────────────────────────────────────────────────────────

def main():
    # Stage 1 + 2 — Normalize & deduplicate every resume
    normalized = {name: normalize_skills(raw) for name, raw in RESUMES.items()}

    # Stage 3 — Build shared vocabulary
    vocab = build_vocabulary(normalized)

    # Stage 4 — Compute TF-IDF vectors for resumes
    tfidf_vectors = compute_tfidf_vectors(normalized, vocab)

    # Stage 5 + 6 — Build JD vectors, rank, print top-3
    print("=" * 50)
    print("  FINAL OUTPUT")
    print("=" * 50)

    for jd_id, jd_info in JDS.items():
        jd_vec  = build_jd_vector(jd_info, vocab)
        ranked  = rank_candidates(tfidf_vectors, jd_vec)
        top3    = ranked[:3]
        result  = ", ".join(f"{name}({score:.2f})" for name, score in top3)

        print(f"\n{jd_info['label']}")
        print(result)

    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
