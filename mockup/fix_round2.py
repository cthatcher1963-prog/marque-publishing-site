# -*- coding: utf-8 -*-
import os
H = os.path.dirname(os.path.abspath(__file__))
def rw(name, pairs):
    p = os.path.join(H, name); t = open(p, encoding='utf-8').read()
    for a, b in pairs:
        assert a in t, ('missing', name, a[:60])
        t = t.replace(a, b)
    open(p, 'w', encoding='utf-8', newline='\n').write(t); print('ok', name)

rw('home-main.html', [
    # 1. Same type as the hero paragraph: reuse .hero-sub for the appended copy
    ('.hero-invite { max-width: 40rem; margin-top: 1.5rem; color: #C9CFD6; font-size: 1.02rem; line-height: 1.7; }\n.hero-invite p { margin-bottom: 0.9rem; }\n.hero-invite a { color: #E8E4DC; border-bottom: 1px solid rgba(232,228,220,0.35); }\n.hero-invite a:hover { color: var(--brass); border-bottom-color: var(--brass); }\n',
     '.hero-invite p.hero-sub { margin-top: 1rem; }\n'),
    # 2. One way to reach you: plain prose, one button
    ('<p>We hope you\'ll join us on this adventure. <a href="mailto:chris@marquepublishing.com">Email us</a> and tell us what you\'re building, what else you\'d like to see from us, and, of course, what you think of our work.</p>',
     '<p class="hero-sub">We hope you\'ll join us on this adventure. Email us and tell us what you\'re building, what else you\'d like to see from us, and, of course, what you think of our work.</p>'),
    ('<p>If you\'re an author struggling with your project, we can help. We can\'t offer the name recognition of a big label, but we will give you personalized service and help you get published. We can even give you your own author page. <a href="mailto:chris@marquepublishing.com?subject=Publishing%20services">Contact us</a> for more information.</p>',
     '<p class="hero-sub">If you\'re an author struggling with your project, we can help. We can\'t offer the name recognition of a big label, but we will give you personalized service and help you get published. We can even give you your own author page. Contact us for more information.</p>'),
    # credentials: dot after each item, not before, so a wrap never starts with a dot
    ('.publisher-creds span + span::before { content: \'\\00B7\'; margin-right: 1.25rem; color: var(--text-subtle); }',
     '.publisher-creds span:not(:last-child)::after { content: \'\\00B7\'; margin-left: 1.25rem; color: var(--text-subtle); }'),
])

rw('labs-engineer.html', [
    ('<span>Software</span><span>Game development</span><span>Head of Marque Labs</span>',
     '<span>Software</span><span>Games</span><span>Head of Marque Labs</span>'),
    ('.engineer-creds span + span::before { content: \'\\00B7\'; margin-right: 1.25rem; color: var(--text-subtle); }',
     '.engineer-creds span:not(:last-child)::after { content: \'\\00B7\'; margin-left: 1.25rem; color: var(--text-subtle); }'),
    ('<p>He came to AI the way a lot of developers do: wanting nothing to do with it writing his code. He came around when it started helping with the problems that had him stuck, and now it\'s part of how he works. What he\'s building is coming soon. When it ships, it\'ll be something he\'d play himself.</p>',
     '<p>He came to AI the way a lot of developers do: wanting nothing to do with it writing his code. He came around when it started helping with the problems that had him stuck, but he still prefers to write his own code. He loves gaming, anime, and vocaloid and synth music. When he is not writing code or watching <em>One Piece</em> with Dad, he is probably playing in a Pok&eacute;mon tournament.</p>\n        <p>He started programming in Scratch when he was 7 and earned his Black Belt at Code Ninjas when he was 15. He codes in Lua, Java, JavaScript, C#, and Python and builds games in Unity and Godot.</p>\n        <p>What he\'s building is coming soon. When it ships, it\'ll be something he\'d play himself.</p>'),
])
