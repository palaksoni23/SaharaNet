content = open('app.py', encoding='utf-8').read()

# Remove old voice component (jo upar tha)
old = '''# ── VOICE JAVASCRIPT ──────────────────────────────────────────
st.components.v1.html("""'''

# Find and replace karo
import re
# Remove entire voice component block
content = re.sub(
    r'# ── VOICE JAVASCRIPT ──.*?""", height=70\)',
    '',
    content,
    flags=re.DOTALL
)

# Voice button chat input ke BAAD add karo
old2 = 'user_input = st.chat_input("Describe what you see… (Hindi / English / Hinglish)")'

new2 = '''# Voice button
st.markdown("""
<div style="display:flex;justify-content:center;margin:8px 0 4px;">
    <button onclick="startVoice()"
        id="voiceBtn"
        style="background:rgba(0,201,177,.08);border:1px solid rgba(0,201,177,.3);
               color:#00C9B1;font-size:12px;font-weight:600;
               padding:8px 20px;border-radius:100px;cursor:pointer;">
        🎤 Voice se bolo
    </button>
</div>
<script>
function startVoice() {
    var btn = document.getElementById('voiceBtn');
    if (!('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)) {
        alert('Chrome use karo voice ke liye!'); return;
    }
    var SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    var r = new SR();
    r.lang = 'hi-IN';
    r.onstart = function(){ btn.textContent = '🔴 Bol rahe hain...'; btn.style.color='#FF3B5C'; };
    r.onresult = function(e){
        var t = e.results[0][0].transcript;
        var inp = window.parent.document.querySelector('textarea[data-testid="stChatInput"]');
        if(inp){
            Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype,'value').set.call(inp,t);
            inp.dispatchEvent(new Event('input',{bubbles:true}));
            setTimeout(function(){
                var sb = window.parent.document.querySelector('button[data-testid="stChatInputSubmitButton"]');
                if(sb) sb.click();
            }, 400);
        }
    };
    r.onend = function(){ btn.textContent = '🎤 Voice se bolo'; btn.style.color='#00C9B1'; };
    r.start();
}
</script>
""", unsafe_allow_html=True)

user_input = st.chat_input("Describe what you see… (Hindi / English / Hinglish)")'''

content = content.replace(old2, new2)
open('app.py', 'w', encoding='utf-8').write(content)
print("Done!")