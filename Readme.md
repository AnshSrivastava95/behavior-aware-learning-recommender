# Behavior-Aware Learning Recommender

## 📌 Overview

Behavior-Aware Learning Recommender is an adaptive learning system designed to personalize study paths based on student learning behavior. The system analyzes student interaction signals during an initial exploration phase to determine the most effective learning approach — either a focused modality-driven path or a hybrid multi-modality path.

Once a learning strategy is identified, the recommendation engine generates structured learning sequences aligned with the student’s preferred difficulty level and learning style.

This project aims to simulate an intelligent pedagogical engine capable of improving learning efficiency through adaptive content delivery.

---

## 🎯 Objectives

* Discover effective learning approaches for students using behavioral signals
* Generate personalized learning paths based on strategy (Focused / Hybrid)
* Maintain optimal challenge–ability alignment using difficulty-aware ranking
* Provide modular architecture for future integration of GMM clustering and contextual bandit optimization

---

## ⚙️ Current MVP Features

* CSV-based structured content dataset
* Focused recommendation mode (single dominant modality ranking)
* Hybrid recommendation mode (multi-modality diversity selection)
* Difficulty-aware scoring using ability–challenge alignment
* Top-K learning path generation
* Modular strategy-execution architecture

---

## 🧠 System Architecture

```
Exploration Phase (Unit-1)
        ↓
Learning Style Scoring
        ↓
Strategy Selection (Focused / Hybrid)
        ↓
Recommendation Engine
        ↓
Structured Learning Path
```

---

## 📊 Content Schema

Each learning item contains:

* `id` – unique identifier
* `unit` – learning unit/topic
* `modality` – visual / reading / quiz / practice / revision / challenge
* `difficulty` – normalized difficulty score (0–1)

---

## 🚀 Future Improvements

* Difficulty progression based curriculum sequencing
* Learning style discovery using Gaussian Mixture Models (GMM)
* Contextual multi-armed bandit for adaptive policy optimization
* Knowledge state modeling and mastery tracking
* Dynamic content generation for focused learners

---

## 👥 Team Collaboration Workflow

* Feature branches for module development
* Pull request based merging into `main`
* Modular ownership (recommendation, modeling, backend, evaluation)

---

## 📚 Tech Stack

* Python
* Pandas
* Git & GitHub

---

## 📌 Project Status

MVP recommendation engine implemented.
Adaptive strategy inference and intelligent path construction under development.
