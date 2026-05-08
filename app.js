function loadProductionData() {
    const grid = document.getElementById('scene-grid');
    
    try {
        if (typeof PRODUCTION_DATA === 'undefined') {
            throw new Error('데이터 원천을 찾을 수 없습니다.');
        }
        
        const data = PRODUCTION_DATA;
        grid.innerHTML = '';
        
        data.forEach((item, index) => {
            const card = document.createElement('div');
            card.className = 'card';
            card.style.animationDelay = `${index * 0.2}s`;
            
            // 시네마틱 오버레이 구조로 렌더링
            card.innerHTML = `
                <div class="card-image" style="background-image: url('${item.image}')"></div>
                <div class="card-overlay">
                    <div class="card-content">
                        <div class="card-id">SCENE ${String(item.id).padStart(2, '0')}</div>
                        <div class="card-title">${item.original_description}</div>
                        <div class="card-description">${extractEmotion(item.id)}</div>
                        <div class="prompt-box">
                            ${item.generated_prompt}
                        </div>
                    </div>
                </div>
            `;
            
            // 클릭 시 프롬프트 복사 알림 (세련된 피드백 추가)
            card.onclick = () => {
                navigator.clipboard.writeText(item.generated_prompt);
                const originalTitle = card.querySelector('.card-title').innerText;
                card.querySelector('.card-title').innerText = 'PROMPT COPIED!';
                setTimeout(() => {
                    card.querySelector('.card-title').innerText = originalTitle;
                }, 2000);
            };
            
            grid.appendChild(card);
        });
        
    } catch (error) {
        console.error('Error:', error);
        grid.innerHTML = `<p style="color:red; grid-column: 1/-1; text-align: center;">데이터 로딩 오류: ${error.message}</p>`;
    }
}

function extractEmotion(id) {
    const emotions = {
        1: "Mood: Anticipation & Melancholy",
        2: "Mood: Interior Warmth & Solitude",
        3: "Mood: Atmospheric Mystery & Distance",
        4: "Mood: Cinematic Serenity & Finality"
    };
    return emotions[id] || "Atmospheric Masterpiece";
}

document.addEventListener('DOMContentLoaded', loadProductionData);
