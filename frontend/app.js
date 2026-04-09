const API_BASE = "http://127.0.0.1:8000";

// DOM Elements
const inputView = document.getElementById('input-view');
const resultsView = document.getElementById('results-view');
const form = document.getElementById('prediction-form');
const submitBtn = document.getElementById('submitBtn');
const submitText = document.getElementById('submitText');
const submitIcon = document.getElementById('submitIcon');
const submitLoader = document.getElementById('submitLoader');

// Utility to fill mock data
function autoFillMockData() {
    document.getElementById('age').value = 75;
    document.getElementById('bmi').value = 35.2;
    document.getElementById('glucose').value = 195;
    document.getElementById('bp').value = 165;
    document.getElementById('hypertension').value = "1";
    document.getElementById('location').value = "San Francisco";
}

// Reset views
function resetView() {
    resultsView.classList.remove('active-view');
    setTimeout(() => {
        inputView.classList.add('active-view');
    }, 300);
}

function setLoading(isLoading) {
    if (isLoading) {
        submitBtn.disabled = true;
        submitText.innerText = "Analyzing...";
        submitIcon.classList.add('hidden');
        submitLoader.classList.remove('hidden');
    } else {
        submitBtn.disabled = false;
        submitText.innerText = "Generate Analysis";
        submitIcon.classList.remove('hidden');
        submitLoader.classList.add('hidden');
    }
}

function getRiskColor(prob) {
    if (prob < 0.2) return 'var(--success)';
    if (prob < 0.4) return 'var(--warning)';
    return 'var(--danger)';
}

function buildPayload() {
    // We mock building the complex payload required by the backend API 
    // using the simplified fields gathered for the demonstration.
    const age = parseFloat(document.getElementById('age').value);
    const bmi = parseFloat(document.getElementById('bmi').value);
    const glucose = parseFloat(document.getElementById('glucose').value);
    const hypertension = parseInt(document.getElementById('hypertension').value);
    const bp = parseFloat(document.getElementById('bp').value);
    
    // Defaulting missing form features
    const smoking = "smokes";

    return {
        heart: {
            age: age, sex: 1, cp: 3, trestbps: bp, chol: 240, fbs: glucose > 120 ? 1 : 0, 
            restecg: 1, thalach: 140, exang: 1, oldpeak: 1.5, slope: 1, ca: 1, thal: 2
        },
        diabetes: {
            Pregnancies: 0, Glucose: glucose, BloodPressure: bp, SkinThickness: 20,
            Insulin: 80, BMI: bmi, DiabetesPedigreeFunction: 0.5, Age: age
        },
        stroke: {
            gender: "Male", age: age, hypertension: hypertension, heart_disease: 1, 
            ever_married: "Yes", work_type: "Private", Residence_type: "Urban", 
            avg_glucose_level: glucose, bmi: bmi, smoking_status: smoking
        },
        ckd: {
            age: age, bp: bp, sg: 1.015, al: 2, su: 0, rbc: "normal", pc: "abnormal", 
            pcc: "present", ba: "notpresent", bgr: glucose, bu: 40, sc: 1.5, sod: 135, 
            pot: 4.0, hemo: 11.0, pcv: 32, wc: 6000, rc: 4.0, htn: "yes", dm: "yes", 
            cad: "no", appet: "poor", pe: "yes", ane: "yes"
        }
    };
}

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    setLoading(true);

    const payload = buildPayload();
    const loc = document.getElementById('location').value || 'Chicago';

    try {
        const response = await fetch(`${API_BASE}/predict/chri`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!response.ok) throw new Error("API call failed.");
        const data = await response.json();
        
        populateDashboard(data, loc);

        // Switch views
        inputView.classList.remove('active-view');
        setTimeout(() => {
            resultsView.classList.add('active-view');
        }, 400);

    } catch (err) {
        console.error(err);
        alert("Failed to connect to the backend server. Is Python FastAPI running?");
    } finally {
        setLoading(false);
    }
});

function populateDashboard(data, locationString) {
    // 1. Update CHRI
    document.getElementById('resCHRI').innerText = data.chri_score.toFixed(2);
    document.getElementById('resRiskLevel').innerText = data.risk_level;
    
    // Set circle color gradient
    let color = getRiskColor(data.chri_score);
    document.getElementById('chriCircle').style.background = `conic-gradient(${color} ${data.chri_score * 100}%, rgba(255,255,255,0.05) 0%)`;

    // 2. Map Probabilities
    const diseases = [
        { name: "Stroke Risk", val: data.stroke },
        { name: "Heart Disease", val: data.heart },
        { name: "Diabetes", val: data.diabetes },
        { name: "Chronic Kidney Disease", val: data.ckd }
    ];
    
    const dList = document.getElementById('diseaseList');
    dList.innerHTML = "";
    diseases.forEach(d => {
        let percent = (d.val * 100).toFixed(1);
        let barColor = getRiskColor(d.val);
        dList.innerHTML += `
            <div class="prob-item">
                <div class="prob-header">
                    <span>${d.name}</span>
                    <span style="color:${barColor}; font-weight:600">${percent}%</span>
                </div>
                <div class="prob-bar-container">
                    <div class="prob-bar" style="width: ${percent}%; background-color: ${barColor}"></div>
                </div>
            </div>
        `;
    });

    // 3. Actions
    document.getElementById('resUrgency').innerText = data.recommendations.urgency_level;
    let urgClass = 'urgency-low';
    if(data.recommendations.urgency_level.includes("High")) urgClass = 'urgency-mod';
    if(data.recommendations.urgency_level.includes("Urgent")) urgClass = 'urgency-high';
    document.getElementById('resUrgency').className = `urgency-banner ${urgClass}`;
    
    const aList = document.getElementById('actionList');
    aList.innerHTML = "";
    data.recommendations.suggested_actions.forEach(a => {
        aList.innerHTML += `<li>${a}</li>`;
    });

    // 4. Extract global top features (Explainability)
    // We aggregate unique top features from the different models
    const xList = document.getElementById('xaiList');
    xList.innerHTML = "";
    
    // Quick merge
    let extractedFeatures = [];
    Object.values(data.top_features).forEach(modelArr => {
        modelArr.forEach(feat => {
            if(!extractedFeatures.find(f => f.feature === feat.feature)){
                extractedFeatures.push(feat);
            }
        });
    });
    
    // Sort and limit to 4 to keep it minimal
    extractedFeatures.sort((a,b) => a.importance === 'high' ? -1 : 1).slice(0, 4).forEach(f => {
        let badgeClass = f.importance === 'high' ? 'xai-high' : 'xai-medium';
        xList.innerHTML += `
            <div class="xai-item">
                <div class="xai-feature"><i class="fa-solid fa-square-caret-right" style="color:var(--text-muted); margin-right:8px"></i> ${f.feature.replace(/_/g, ' ')}</div>
                <div class="xai-badge ${badgeClass}">${f.importance} Impact</div>
            </div>
        `;
    });

    // 5. Render Doctors / Facilities (we fetch facilities async now)
    fetchFacilities(locationString);
}

// Fetch via the backend routing to OpenStreetMap
async function fetchFacilities(locString) {
    const docList = document.getElementById('doctorList');
    docList.innerHTML = `<p style="color:var(--text-muted)">Querying OpenStreetMap APIs for ${locString}...</p>`;
    
    try {
        const response = await fetch(`${API_BASE}/recommend/facilities`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ location: locString })
        });
        const data = await response.json();
        
        docList.innerHTML = "";
        if(data && data.length > 0) {
            data.slice(0, 4).forEach(fac => {
                docList.innerHTML += `
                    <div class="doctor-card">
                        <div class="doctor-spec">Medical Center</div>
                        <h4>${fac.name}</h4>
                        <div class="doctor-loc">
                            <i class="fa-solid fa-location-dot"></i>
                            <span>${fac.address}</span>
                        </div>
                    </div>
                `;
            });
        } else {
            docList.innerHTML = `<p>No facilities found in this exact location. Try adjusting the city.</p>`;
        }
    } catch(err) {
        docList.innerHTML = `<p style="color:var(--danger)">Could not fetch facilities.</p>`;
    }
}
