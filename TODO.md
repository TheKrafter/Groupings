### Things to Do

The complete roadmap for Groupings.

- [ ] Implement UI
    - [ ] Groups list
    - [ ] Former groups list
    - [ ] Messages page
    - [ ] send message dialog
    - [ ] Member list
    - [ ] DMs
- [x] Auth/Login
- [ ] Load Groups
    - [ ] Add/rm groups (func)
    - [ ] List groups in sidebar
        - [ ] with Icons
    - [ ] Switch message pane to that group
    - [ ] List of former groups
- [ ] Load Messages in Group
    - [ ] Message
        - [ ] Text
        - [ ] Author
        - [ ] Attachments
        - [ ] Emojis! [how to display](https://github.com/GeopJr/Tuba/issues/622#issuecomment-1781663957) and [GroupyAPI docs for emojis](https://groupy.readthedocs.io/en/latest/pages/api.html?highlight=emoji#groupy.api.attachments.Emoji)
        - [ ] Likes (w/ func to add/rm by msg ID & user)
    - [ ] List of groups in message pane
    - [ ] func to add messages
    - [ ] func to rm/edit messages (by ID)
- [ ] Push
    - [ ] add messages + likes to currently open Group
    - [ ] Notifications
        - [ ] Messages + likes sent in not open group (click notif to switch?)
        - [ ] Messages + likes sent in all groups when we don't have focus
        - [ ] Ignore messages sent by self
- [ ] Send messages
    - NOTE: Do NOT add messages manually to the messages list.
    - [ ] Ensure msg is sent in current selected group
    - [ ] Send contents of input box
    - [ ] Attachments
        - [ ] File chooser portal
        - [ ] Upload file
        - [ ] attach to message
    - [ ] Sending Emojis?

- [x] Packaging
    - [x] Icon
    - [x] `.desktop` file
    - [x] Flatpak

### Things to NOTE!

- EVERYTHING must be modular (including GUI)!
- Create with running in background in mind
- Use flatpak-isms in hopes of Flatpaking later (i.e. `xdg-desktop-portals`) [?](https://pypi.org/project/desktop3/)
