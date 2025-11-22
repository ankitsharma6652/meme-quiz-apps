document.addEventListener('DOMContentLoaded', () => {
    const viewTrendingBtn = document.getElementById('view-trending-btn');
    const resultContainer = document.getElementById('result-container');
    const loadingDiv = document.getElementById('loading');
    const memeFeed = document.getElementById('meme-feed');
    const closeResultsBtn = document.getElementById('close-results');

    console.log('Script loaded. Elements:', {
        viewTrendingBtn,
        resultContainer,
        loadingDiv,
        memeFeed,
        closeResultsBtn
    });

    // Helper to show/hide elements
    const show = (el) => {
        if (el) el.classList.remove('hidden');
    };
    const hide = (el) => {
        if (el) el.classList.add('hidden');
    };

    // --- TRENDING MEMES ---
    viewTrendingBtn.addEventListener('click', async () => {
        console.log('Button clicked!');

        show(resultContainer);
        show(loadingDiv);
        hide(memeFeed);
        hide(closeResultsBtn);

        // Clear previous feed
        memeFeed.innerHTML = '';

        try {
            console.log('Fetching memes...');
            const response = await fetch('/api/trending-memes');
            console.log('Response status:', response.status);

            if (!response.ok) throw new Error('Failed to fetch trending memes');

            const memes = await response.json();
            console.log(`Received ${memes.length} memes`);

            renderFeed(memes);

        } catch (error) {
            console.error('Error:', error);
            alert('Failed to load trending memes. Please try again.');
            hide(resultContainer);
        } finally {
            hide(loadingDiv);
        }
    });

    function renderFeed(memes) {
        console.log('renderFeed called with', memes.length, 'memes');

        // Clear and show
        memeFeed.innerHTML = '';
        memeFeed.style.display = 'flex';
        memeFeed.style.flexDirection = 'column';
        memeFeed.style.gap = '2rem';
        memeFeed.style.width = '100%';

        show(memeFeed);
        show(closeResultsBtn);

        if (!memes || memes.length === 0) {
            memeFeed.innerHTML = '<div style="text-align:center; padding:2rem; color:white; background:#333; border-radius:10px;">No viral content found. Try again!</div>';
            return;
        }

        memes.forEach((meme, index) => {
            console.log(`Rendering meme ${index + 1}:`, meme.title);

            const post = document.createElement('div');
            post.className = 'meme-post';
            post.style.display = 'flex';
            post.style.flexDirection = 'column';
            post.style.background = '#1a1a1f';
            post.style.borderRadius = '15px';
            post.style.overflow = 'hidden';
            post.style.border = '1px solid #333';

            // Header
            const header = document.createElement('div');
            header.className = 'meme-header';
            header.style.padding = '1rem';
            header.style.borderBottom = '1px solid #333';
            header.innerHTML = `
                <h3 style="margin:0; color:white; font-size:1.1rem;">${meme.title}</h3>
                <div style="color:#aaa; font-size:0.8rem; margin-top:0.3rem;">@${meme.author}</div>
            `;
            post.appendChild(header);

            // Media
            const mediaDiv = document.createElement('div');
            mediaDiv.className = 'meme-media';
            mediaDiv.style.background = '#000';
            mediaDiv.style.minHeight = '200px';
            mediaDiv.style.display = 'flex';
            mediaDiv.style.alignItems = 'center';
            mediaDiv.style.justifyContent = 'center';
            mediaDiv.style.padding = '10px';

            if (meme.is_video && meme.video_url) {
                console.log('Adding video:', meme.video_url);
                const video = document.createElement('video');
                video.controls = true;
                video.loop = true;
                video.muted = true;
                video.playsInline = true;
                video.preload = 'metadata';
                video.style.width = '100%';
                video.style.maxHeight = '600px';
                video.style.display = 'block';

                const source = document.createElement('source');
                source.src = meme.video_url;
                source.type = 'video/mp4';

                video.appendChild(source);
                mediaDiv.appendChild(video);
            } else {
                console.log('Adding image:', meme.url);
                const img = document.createElement('img');
                img.src = meme.url;
                img.alt = meme.title;
                img.loading = 'lazy';
                img.style.maxWidth = '100%';
                img.style.maxHeight = '600px';
                img.style.display = 'block';
                img.style.margin = '0 auto';
                img.onerror = function () {
                    console.log('Image failed to load:', this.src);
                    this.style.display = 'none';
                };

                mediaDiv.appendChild(img);
            }
            post.appendChild(mediaDiv);

            // Footer
            const footer = document.createElement('div');
            footer.className = 'meme-footer';
            footer.style.padding = '1rem';
            footer.style.borderTop = '1px solid #333';
            footer.style.display = 'flex';
            footer.style.justifyContent = 'space-between';
            footer.style.color = '#aaa';
            footer.innerHTML = `
                <span>⬆️ ${meme.ups.toLocaleString()}</span>
                <a href="${meme.permalink}" target="_blank" style="color: #00d2ff; text-decoration: none;">🔗 Source</a>
            `;
            post.appendChild(footer);

            memeFeed.appendChild(post);
        });

        console.log('Rendering complete!');
    }

    closeResultsBtn.addEventListener('click', () => {
        hide(resultContainer);
        memeFeed.innerHTML = '';
    });

    // 3D Tilt Effect
    const cards = document.querySelectorAll('.card, .hero-card');
    cards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            const rotateX = ((y - centerY) / centerY) * -5;
            const rotateY = ((x - centerX) / centerX) * 5;
            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(1.02)`;
        });
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) scale(1)';
        });
    });
});
