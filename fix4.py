content = open('app.py', encoding='utf-8').read()

# Pehle purana voice html dhundho aur hatao
import re
content = re.sub(r'# Voice button\nst\.markdown\(""".*?unsafe_allow_html=True\)\n\n', '', content, flags=re.DOTALL)

# Ab chat_input ke NEECHE inject karo
old = 'if user_input:'
new = '''col1, col2 = st.columns([4, 1])
with col2:
    if st.button("🎤", help="Voice se bolo", use_container_width=True):
        st.session_state.voice_mode = True

st.components.v1.html("""
<script>
(function() {
    var SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SR) return;
    var r = new SR();
    r.lang = 'hi-IN';
    r.continuous = false;
    r.onresult = function(e) {
        var t = e.results[0][0].transcript;
        var inp = window.parent.document.querySelector('textarea[data-testid="stChatInput"]');
        if (inp) {
            Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype,'value').set.call(inp, t);
            inp.dispatchEvent(new Event('input', {bubbles:true}));
            setTimeout(function(){
                var btn = window.parent.document.querySelector('button[data-testid="stChatInputSubmitButton"]');
                if (btn) btn.click();
            }, 500);
        }
    };
    window._saharaRecognition = r;
})();

function startListening() {
    if (window._saharaRecognition) {
        window._saharaRecognition.start();
    }
}
</script>
""", height=0)

if st.session_state.get("voice_mode"):
    st.session_state.voice_mode = False
    st.components.v1.html("<script>startListening();</script>", height=0)

if user_input:'''

content = content.replace(old, new, 1)
open('app.py', 'w', encoding='utf-8').write(content)
print("Done!")