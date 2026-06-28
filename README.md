# 🏗️ GCIP (Global Construction Intelligence Platform)
**AI-Powered Construction Management & Commercial Intelligence System**

![Status](https://img.shields.io/badge/Status-Development-orange) ![Version](https://img.shields.io/badge/Version-1.0.0-brightgreen) ![Confidential](https://img.shields.io/badge/Visibility-Private-red)

## 📌 Proje Özeti (Executive Summary)
**GCIP**, geleneksel inşaat sektöründeki (AEC) kâr marjı sızıntılarını, hatalı hakedişleri ve manuel metraj süreçlerini otonom yapay zeka ajanları (Multi-Agent AI Swarm) ile çözen yeni nesil bir **İnşaat Ticari Zeka ve Hakediş Otomasyon Platformudur.** 

İnsan hatasını ortadan kaldırarak şantiyelerdeki gizli finansal kayıpları (avans unutulması, haksız zeyilnameler, metot değişiklikleri) otonom olarak tespit eder. "Kirli CAD" dosyalarını okuyabilen geometrik zekası, Primavera P6 kritik yol entegrasyonu ve Neo4j tabanlı RAG mimarisi sayesinde, taşeron ile ana firma arasındaki hak ediş krizlerini başlamadan bitirir.

---

## 📚 Mimari, Strateji ve Yazılım Anayasası (Documentation Index)
Bu depo, GCIP projesinin A'dan Z'ye tüm mühendislik, iş modeli, pazar stratejisi, veri şemaları ve yazılım kod tabanını içerir. Aşağıdaki belgelere tıklayarak ilgili detaylara ulaşabilirsiniz:

### 📑 Çekirdek Mimarisi ve Temel Belgeler (Docs 0 - 10)
1. [📖 0. Proje Bağlamı (Project Context)](./0.%20PROJECT_CONTEXT.md) - Oturum hafızası ve kararların loglandığı çekirdek günlük.
2. [🚀 1. Vizyon ve Değer Önerisi](./1.%20VISION.md) - Ürün DNA'sı ve vizyonu.
3. [🔥 2. İnşaat Sektöründeki Temel Sorunlar](./2.%20PROBLEMS.md) - Sahadaki değişim direnci ve sektörel kayıplar.
4. [⚠️ 3. Risk Taksonomisi (Risk Taxonomy)](./3.%20RISK_TAXONOMY.md) - Proje risk kategorileri ve risk eşikleri.
5. [🧠 4. Yapay Zeka Mühendislik Bilgi Bankası](./4.%20ENGINEERING_KNOWLEDGE_BASE.md) - RAG mimarisi ve mühendislik hafızası.
6. [👥 5. Kullanıcı Personaları](./5.%20USER_PERSONAS.md) - Kullanıcı profilleri ve arayüz ekosistemi.
7. [⚔️ 6. Rakip Analizi (Procore, Buildots vs.)](./6.%20COMPETITOR_ANALYSIS.md) - Rakiplerin zayıf yönleri ve rekabet avantajları.
8. [🏗️ 7. MVP ve Evrimsel Mimari (Evolutionary Architecture)](./7.%20MVP_AND_EVOLUTIONARY_ARCHITECTURE.md) - KOBİ odaklı MVP kapsamı ve evrimsel mimari adımları.
9. [💰 8. İş Modeli ve Pazara Giriş Stratejisi (GTM)](./8.%20BUSINESS_MODEL_AND_GTM.md) - Gelir modelleri, pazar sızma taktikleri ve GTM planı.
10. [🔒 9. Veri Güvenliği ve Kurumsal İzolasyon (Data Security)](./9.%20DATA_SECURITY_AND_PRIVACY.md) - Zero-knowledge ve multi-tenant veri güvenliği.
11. [⚙️ 10. Teknoloji Yığını ve 18 Aylık Yol Haritası (Tech Stack)](./10.%20TECH_STACK_AND_ROADMAP.md) - Temel teknoloji yığını ve 18 aylık yol haritası.

### 📑 Stratejik İnceleme ve Yasal Uyum (Docs 11 - 18)
12. [💳 11. Fiyatlandırma Modeli (Pricing Model)](./11.%20PRICING_MODEL.md) - Proje bazlı KOBİ SaaS paketleri ve kullanım bazlı AI tarifesi.
13. [📊 12. Stratejik Değerlendirme (Strategic Review)](./12.%20STRATEGIC_REVIEW.md) - 18 aylık hedefler, M&A çıkış planı ve 11 fazlık master yol haritası.
14. [🎯 13. Ürün Konumlandırma](./13.%20PRODUCT_POSITIONING.md) - GTM pazara giriş ve "Truva Atı" sızma taktikleri.
15. [🔒 14. Güvenlik ve KVKK/GDPR Uyum](./14.%20SECURITY_COMPLIANCE.md) - Askeri düzeyde çoklu kiracı (multi-tenant) izolasyonu ve zaman damgası.
16. [🔌 15. Entegrasyon Haritası (Integration Map)](./15.%20INTEGRATION_MAP.md) - Çekirdek (KOBİ) ve kurumsal API entegrasyon katmanları.
17. [🔔 16. Bildirim Stratejisi (Notification Strategy)](./16.%20NOTIFICATION_STRATEGY.md) - Çok kanallı alarm matrisi ve eskalasyon kuralları.
18. [🔄 17. İş Akışları ve Gölge Modu (Workflows)](./17.%20WORKFLOWS.md) - Ajanların adım adım karar akışları ve Shadow Mode işletimi.
19. [🌳 18. Karar Verme Çerçevesi (Decision Framework)](./18.%20DECISION_FRAMEWORK.md) - Vinç telemetri, zemin delgi sapması ve 72 saatlik yasal İSG karar ağaçları.

### 📑 Ajan Swarm ve Veri Modeli Altyapısı (Docs 19 - 27)
20. [🤖 19. Yapay Zeka Ajan Rolleri (Agents)](./19.%20AGENTS.md) - Swarm yapısı (QS, Delay Analyst, Safety Agent) yetki ve prompt şablonları.
21. [🕸️ 20. Neo4j Vektör ve Grafik Veri Modeli](./20.%20DATA_MODEL.md) - 33 evrensel disiplin, Cypher şemaları ve APOC kısıtları.
22. [🔗 21. Orkestratör Tasarımı (Orchestrator)](./21.%20ORCHESTRATOR.md) - LangGraph durumu (Shared State), semantik yönlendirme ve kontrol döngüsü.
23. [👥 22. İnsan Onay Döngüsü (Feedback Loop / RLHF)](./22.%20FEEDBACK_LOOP.md) - İnsan müdahalesiyle AI kalibrasyonu ve RLHF protokolü.
24. [🖥️ 23. Kullanıcı Arayüzü ve Gösterge Panelleri](./23.%20DASHBOARDS.md) - Ortak Komisyon onay ekranı ve Dashboard arayüz taslakları.
25. [🚀 24. Şantiye Kurulum ve Onboarding](./24.%20ONBOARDING.md) - Baseline kilitleme ve 24 adımlı devreye alma listesi.
26. [📈 25. Başarı Metrikleri (Success Metrics)](./25.%20SUCCESS_METRICS.md) - Ticari, sistemsel, İSG ve kullanıcı benimseme KPI'ları.
27. [📁 27. MVP Kod Klasör Yapısı (Project Structure)](./27.%20PROJECT_STRUCTURE.md) - Monorepo kod dizin yapısı, docker-compose ve Poetry bağımlılıkları.

*Not: 26. MVP_SCOPE belgesi, [7. MVP_AND_EVOLUTIONARY_ARCHITECTURE.md](./7.%20MVP_AND_EVOLUTIONARY_ARCHITECTURE.md) içerisinde harmanlanmıştır.*

---

## 💻 Yazılım ve Kod Tabanı (Codebase)

Kod tabanımız **monorepo** olarak kurgulanmış olup iki ana klasörden oluşur:
*   [📂 `backend/`](./backend/) - FastAPI, Uvicorn, Neo4j, Redis ve LangGraph tabanlı Python arka yüzü.
    *   [📄 `backend/test_rag.py`](./backend/test_rag.py) - RAG ve Neo4j Vector Search entegrasyonunun uçtan uca doğrulanması için E2E test paketi.
*   [📂 `frontend/`](./frontend/) - RxDB çevrimdışı yerel veritabanı entegrasyonlu React PWA ön yüz bileşenleri ve gösterge panelleri.
*   [📂 `docker/`](./docker/) - Neo4j Enterprise, Redis ve yerel Llama-3 çalıştıran orkestrasyon (`docker-compose.yml`) dosyaları.

---
*Bu dokümantasyon özel mülkiyettir (Proprietary & Confidential) ve GCIP kurucularının izni olmadan kopyalanamaz, paylaşılamaz.*
