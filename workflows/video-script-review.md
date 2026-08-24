# Video Script Review

**Version**: 0.1  
**Status**: Draft

## Prerequisite

`parsed_note.status=approved`.

## Flow

1. Generate the script from the approved parsed-note revision.
2. Create or update the video script child document.
3. Set `video_script.status=pending_review`.
4. Send a dedicated `视频脚本待审核` Feishu message with the document link.
5. On approval, set `video_script.status=approved`.
6. On change request, revise only the video document, increment its revision, and send a new video reminder.

## Review Checklist

- The script can be spoken naturally and has a concrete opening.
- Facts and dialogue remain faithful to the approved parsed note.
- Privacy-sensitive details are acceptable for video publication.
- The final insight is restrained and sounds like the user.
