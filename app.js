// Initialize Lucide icons
lucide.createIcons();

// Tab Switching Logic
function switchTab(tabName) {
    const sections = ['dashboard', 'analytics', 'settings'];
    sections.forEach(s => {
        document.getElementById(`tab-${s}`).classList.add('hidden');
        document.getElementById(`nav-${s}`).classList.remove('active');
    });

    document.getElementById(`tab-${tabName}`).classList.remove('hidden');
    document.getElementById(`nav-${tabName}`).classList.add('active');

    if (tabName === 'analytics') {
        initCharts();
    }
}

// Live Preview Logic
const captionInput = document.getElementById('post-caption');
const previewTexts = {
    instagram: document.getElementById('preview-text-instagram'),
    facebook: document.getElementById('preview-text-facebook'),
    linkedin: document.getElementById('preview-text-linkedin'),
    youtube: document.getElementById('preview-text-youtube')
};

captionInput.addEventListener('input', updatePreview);

function setPreviewPlatform(platform) {
    // Update tabs
    document.querySelectorAll('.preview-tab').forEach(btn => {
        btn.classList.remove('active');
    });
    event.currentTarget.classList.add('active');

    // Update visibility
    document.querySelectorAll('.mockup-content').forEach(el => {
        el.classList.add('hidden');
    });
    document.getElementById(`preview-${platform}`).classList.remove('hidden');
}

// Charting Logic
let perfChart, distChart;
async function initCharts() {
    if (perfChart) perfChart.destroy();
    if (distChart) distChart.destroy();

    try {
        const response = await fetch('http://127.0.0.1:8000/api/analytics');
        const data = await response.json();

        const ctxPerf = document.getElementById('performanceChart').getContext('2d');
        perfChart = new Chart(ctxPerf, {
            type: 'line',
            data: {
                labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                datasets: [{
                    label: 'Reach',
                    data: data.reach,
                    borderColor: '#6366F1',
                    backgroundColor: 'rgba(99, 102, 241, 0.1)',
                    fill: true,
                    tension: 0.4,
                    borderWidth: 3,
                    pointRadius: 4,
                    pointBackgroundColor: '#6366F1'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    y: { grid: { color: 'rgba(255, 255, 255, 0.05)' }, ticks: { color: 'rgba(255, 255, 255, 0.4)' } },
                    x: { grid: { display: false }, ticks: { color: 'rgba(255, 255, 255, 0.4)' } }
                }
            }
        });

        const ctxDist = document.getElementById('distributionChart').getContext('2d');
        distChart = new Chart(ctxDist, {
            type: 'doughnut',
            data: {
                labels: ['Instagram', 'Facebook', 'LinkedIn', 'YouTube'],
                datasets: [{
                    data: data.engagement,
                    backgroundColor: ['#EC4899', '#3B82F6', '#0EA5E9', '#EF4444'],
                    borderWidth: 0,
                    hoverOffset: 10
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: 'rgba(255, 255, 255, 0.6)',
                            padding: 20,
                            font: { size: 12 }
                        }
                    }
                },
                cutout: '70%'
            }
        });
    } catch (error) {
        console.error('Failed to load analytics:', error);
    }
}

// Drag and Drop Logic
const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');
let selectedFiles = [];

dropZone.onclick = () => fileInput.click();

dropZone.ondragover = (e) => {
    e.preventDefault();
    dropZone.classList.add('border-indigo-500');
};

dropZone.ondragleave = () => {
    dropZone.classList.remove('border-indigo-500');
};

dropZone.ondrop = (e) => {
    e.preventDefault();
    dropZone.classList.remove('border-indigo-500');
    handleFiles(e.dataTransfer.files);
};

fileInput.onchange = (e) => {
    handleFiles(e.target.files);
};

function handleFiles(files) {
    selectedFiles = Array.from(files);
    console.log('Files selected:', selectedFiles);
    validatePlatforms();
    
    // Update UI to show filename
    if (selectedFiles.length > 0) {
        const text = dropZone.querySelector('p:first-of-type');
        text.innerText = `${selectedFiles.length} file(s) selected: ${selectedFiles[0].name}`;
        
        // Update Preview Media
        const file = selectedFiles[0];
        const reader = new FileReader();
        
        reader.onload = (e) => {
            const url = e.target.result;
            const containers = ['preview-media-container', 'preview-media-fb', 'preview-media-li', 'preview-media-yt'];
            
            containers.forEach(id => {
                const el = document.getElementById(id);
                if (!el) return;
                
                if (file.type.startsWith('image')) {
                    el.innerHTML = `<img src="${url}" class="w-full h-full object-cover">`;
                } else if (file.type.startsWith('video')) {
                    el.innerHTML = `<video src="${url}" class="w-full h-full object-cover" autoplay muted loop></video>`;
                    if (id === 'preview-media-yt') {
                         el.innerHTML += `<div class="absolute inset-0 bg-black/20 flex items-center justify-center"><i data-lucide="play" class="w-8 h-8 text-white"></i></div>`;
                         lucide.createIcons();
                    }
                }
            });
            // Auto-save media to draft
            saveDraft(true);
        };
        
        reader.readAsDataURL(file);
    }
}

// Validation Logic (YouTube Requirement)
function validatePlatforms() {
    const ytCheckbox = document.getElementById('yt-checkbox');
    const ytWarning = document.getElementById('yt-warning');
    const publishBtn = document.getElementById('publish-btn');
    
    let hasVideo = selectedFiles.some(f => f.type.includes('video'));
    
    if (ytCheckbox.checked && !hasVideo) {
        ytWarning.classList.remove('hidden');
        publishBtn.disabled = true;
        publishBtn.classList.add('opacity-50', 'cursor-not-allowed');
    } else {
        ytWarning.classList.add('hidden');
        publishBtn.disabled = false;
        publishBtn.classList.remove('opacity-50', 'cursor-not-allowed');
    }
}

// Publish Logic (Mock)
// Publish Logic (Real API)
async function publishContent() {
    const btn = document.getElementById('publish-btn');
    const originalContent = btn.innerHTML;
    
    // Get selected platforms
    const platforms = Array.from(document.querySelectorAll('input[name="platform"]:checked'))
        .map(cb => cb.value)
        .join(',');

    if (!platforms) {
        alert("Please select at least one platform.");
        return;
    }

    const caption = document.getElementById('post-caption').value;
    const hashtagContainer = document.getElementById('hashtag-container');
    const hashtags = Array.from(hashtagContainer.querySelectorAll('span:not(#hashtag-input)'))
        .map(el => el.innerText.trim())
        .join(' ');

    btn.innerHTML = '<i data-lucide="refresh-cw" class="w-5 h-5 animate-spin"></i> Processing...';
    lucide.createIcons();
    btn.disabled = true;

    try {
        const formData = new FormData();
        formData.append('caption', caption);
        formData.append('hashtags', hashtags);
        formData.append('platforms', platforms);
        if (selectedFiles.length > 0) {
            formData.append('media', selectedFiles[0]);
        }

        const response = await fetch('http://127.0.0.1:8000/api/publish', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        console.log('Publish result:', data);
        
        showToast();
        resetForm();
    } catch (error) {
        console.error('Publish failed:', error);
        alert('Failed to publish. Is the backend running?');
    } finally {
        btn.innerHTML = originalContent;
        btn.disabled = false;
        lucide.createIcons();
    }
}

function showToast() {
    const toast = document.getElementById('success-toast');
    toast.classList.remove('translate-y-20', 'opacity-0');
    
    setTimeout(() => {
        toast.classList.add('translate-y-20', 'opacity-0');
    }, 4000);
}

function resetForm() {
    document.getElementById('post-caption').value = '';
    Object.values(previewTexts).forEach(el => {
        if (el) el.innerText = 'Your caption will appear here...';
    });
    
    const containers = ['preview-media-container', 'preview-media-fb', 'preview-media-li', 'preview-media-yt'];
    containers.forEach(id => {
        const el = document.getElementById(id);
        if (el) el.innerHTML = '<i data-lucide="image" class="w-8 h-8 text-white/10"></i>';
    });
    lucide.createIcons();

    selectedFiles = [];
    dropZone.querySelector('p:first-of-type').innerText = 'Drag & drop images or video';
    validatePlatforms();
}

// Hashtag Logic
const hashtagInput = document.getElementById('hashtag-input');
const hashtagContainer = document.getElementById('hashtag-container');

hashtagInput.onkeydown = (e) => {
    if (e.key === 'Enter' && hashtagInput.value.trim()) {
        e.preventDefault();
        let value = hashtagInput.value.trim();
        // Auto-prefix with # if not present
        if (!value.startsWith('#')) {
            value = '#' + value;
        }
        
        const tag = document.createElement('span');
        tag.className = 'px-3 py-1 rounded-full bg-indigo-500/10 text-indigo-400 text-xs border border-indigo-500/20 flex items-center gap-2 group animate-fade-in';
        tag.innerHTML = `<span>${value}</span> <i data-lucide="x" class="w-3 h-3 cursor-pointer opacity-50 group-hover:opacity-100 transition-all" onclick="this.parentElement.remove(); updatePreview()"></i>`;
        hashtagContainer.insertBefore(tag, hashtagInput);
        hashtagInput.value = '';
        lucide.createIcons();
        updatePreview();
        saveDraft(true);
    }
};

// Helper to update all previews
function updatePreview() {
    const text = captionInput.value || 'Your caption will appear here...';
    const hashtags = Array.from(hashtagContainer.querySelectorAll('span:not(#hashtag-input)'))
        .map(el => el.innerText.trim())
        .join(' ');

    const fullContent = text + (hashtags ? '\n\n' + hashtags : '');

    Object.values(previewTexts).forEach(el => {
        if (el) {
            if (el.id === 'preview-text-youtube') {
                el.innerText = text; // Youtube usually shows title separate from description
            } else {
                el.innerText = fullContent;
            }
        }
    });
}

captionInput.addEventListener('input', updatePreview);

// Mouse move for ambient glow
document.addEventListener('mousemove', (e) => {
    const cards = document.querySelectorAll('.glass-card');
    cards.forEach(card => {
        const rect = card.getBoundingClientRect();
        const x = ((e.clientX - rect.left) / rect.width) * 100;
        const y = ((e.clientY - rect.top) / rect.height) * 100;
        card.style.setProperty('--mouse-x', `${x}%`);
        card.style.setProperty('--mouse-y', `${y}%`);
    });
});

// Draft Persistence Logic
async function saveDraft(isAutoSave = false) {
    const caption = document.getElementById('post-caption').value;
    const platforms = Array.from(document.querySelectorAll('input[name="platform"]:checked'))
        .map(cb => cb.value);
    const hashtags = Array.from(hashtagContainer.querySelectorAll('span:not(#hashtag-input)'))
        .map(el => el.innerText.trim());

    const draft = { caption, platforms, hashtags };

    // Handle Media Persistence (Store as Base64 in draft)
    if (selectedFiles.length > 0) {
        const file = selectedFiles[0];
        draft.mediaName = file.name;
        draft.mediaType = file.type;
        
        // Convert to base64 if it's small enough (roughly < 4MB)
        if (file.size < 4 * 1024 * 1024) {
            try {
                draft.mediaData = await new Promise((resolve, reject) => {
                    const reader = new FileReader();
                    reader.onload = (e) => resolve(e.target.result);
                    reader.onerror = reject;
                    reader.readAsDataURL(file);
                });
            } catch (e) {
                console.warn("Could not save media to draft", e);
            }
        }
    }

    try {
        localStorage.setItem('socialProDraft', JSON.stringify(draft));
        if (!isAutoSave) {
            showDraftToast();
        }
    } catch (e) {
        console.warn("Draft too large for localStorage, saving without media");
        delete draft.mediaData;
        localStorage.setItem('socialProDraft', JSON.stringify(draft));
    }
}

function showDraftToast() {
    const toast = document.getElementById('success-toast');
    const toastTitle = toast.querySelector('p:first-of-type');
    const toastSub = toast.querySelector('p:last-of-type');
    
    const originalText = toastTitle.innerText;
    const originalSub = toastSub.innerText;
    
    toastTitle.innerText = "Draft Saved";
    toastSub.innerText = "Your post has been saved locally";
    
    showToast();
    
    setTimeout(() => {
        toastTitle.innerText = originalText;
        toastSub.innerText = originalSub;
    }, 5000);
}

async function loadDraft() {
    const draftJson = localStorage.getItem('socialProDraft');
    if (!draftJson) return;

    try {
        const draft = JSON.parse(draftJson);
        
        // Load caption
        document.getElementById('post-caption').value = draft.caption || '';
        
        // Load platforms
        const allPlatforms = document.querySelectorAll('input[name="platform"]');
        allPlatforms.forEach(cb => {
            cb.checked = (draft.platforms || []).includes(cb.value);
        });
        
        // Load hashtags
        Array.from(hashtagContainer.querySelectorAll('span:not(#hashtag-input)')).forEach(el => el.remove());
        (draft.hashtags || []).forEach(value => {
            const tag = document.createElement('span');
            tag.className = 'px-3 py-1 rounded-full bg-indigo-500/10 text-indigo-400 text-xs border border-indigo-500/20 flex items-center gap-2 group animate-fade-in';
            tag.innerHTML = `<span>${value}</span> <i data-lucide="x" class="w-3 h-3 cursor-pointer opacity-50 group-hover:opacity-100 transition-all" onclick="this.parentElement.remove(); updatePreview(); saveDraft(true)"></i>`;
            hashtagContainer.insertBefore(tag, hashtagInput);
        });
        
        // Load Media
        if (draft.mediaData) {
            const res = await fetch(draft.mediaData);
            const blob = await res.blob();
            const file = new File([blob], draft.mediaName, { type: draft.mediaType });
            
            // This will trigger the handleFiles logic (previews + state)
            handleFiles([file]);
        }
        
        lucide.createIcons();
        updatePreview();
        validatePlatforms();
    } catch (e) {
        console.error("Failed to load draft:", e);
    }
}

// Auto-save triggers for caption and platforms
captionInput.addEventListener('input', () => {
    saveDraft(true);
});

document.querySelectorAll('input[name="platform"]').forEach(cb => {
    cb.addEventListener('change', () => {
        saveDraft(true);
    });
});

// Start on Dashboard
switchTab('dashboard');
loadDraft();
updatePreview();
