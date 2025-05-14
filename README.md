# MediCall

An AI-powered Emergency Room Matching System connecting emergency patients to the nearest available hospital in seconds.

---

## 🚑 Project Overview

MediCall is a real-time hospital matching system designed for use during emergency patient transport.  
Instead of making manual phone calls to check hospital availability, paramedics can simply enter the patient’s condition and location.  
MediCall uses AI to identify suitable nearby hospitals and automatically initiates parallel voice calls.  
The first hospital to respond is immediately recommended—saving time, reducing uncertainty, and helping protect the patient’s golden hour.

---

## 🛠 Key Features

- AI-powered hospital matching based on patient condition and location  
- Symptom summarization and filtering using Gemini  
- Nearby hospital search via Google Places API  
- Parallel hospital calling and voice response handling with Twilio  
- Real-time navigation to the selected hospital  
- Secure access for certified emergency responders

---

## 🔁 Service Flow

```
[Paramedics - Mobile App] 
  → Send patient condition and location
       ↓
[Server - Gemini AI] 
  → Select hospital list and generate guidance message
       ↓
[Twilio] 
  → Parallel calls; hospital responds with dial (1: Accept / 2: Reject)
       ↓
[Analyze response results + calculate distance]
       ↓
[Final hospital recommendation + route guidance]
```

---

## 🧠 System Description

- **AI-powered hospital matching**  
  Matches emergency patients to nearby hospitals based on real-time location and condition.

- **Gemini-based AI processing**  
  Uses Gemini AI to summarize patient symptoms into concise messages, estimate driving distance and travel time, and determine hospital suitability based on condition and name.

- **Google Places API integration**  
  Searches for nearby hospitals using current latitude, longitude, and radius parameters, and retrieves hospital name, phone number, address, and coordinates.

- **Parallel hospital calling with Twilio**  
  Sends automated voice calls to multiple hospitals at once, enabling them to respond by pressing 1 (accept) or 2 (reject).

- **Navigation to selected hospital**  
  After a hospital is selected based on response and distance, the system provides a route and estimated travel time to the location.

- **Mobile interface**  
  Provides a clean and intuitive UI for emergency responders to quickly enter patient information and receive guidance.

- **Secure access control**  
  Only certified EMTs with valid license numbers can access and use the system.

---

## 📧 Contact

**Email**: medicall.developer@gmail.com
