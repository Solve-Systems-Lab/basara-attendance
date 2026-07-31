/* OWNER: FE track — BALAJI.
 *
 * This is the screen the whole course is about. Port the camera and
 * geolocation logic from the reference app — and only that logic:
 *
 *   pmutwd_attendance/fe/src/app/components/employee/MarkAttendance.tsx:224-332
 *
 * That file is 1,285 lines. About 110 of them matter. Two patterns in it were
 * earned the hard way and are worth keeping exactly as they are:
 *
 *   1. The MediaStream is attached to the <video> element inside a useEffect,
 *      not inside startCamera(). The <video> has not mounted yet at the moment
 *      the stream arrives.
 *   2. Geolocation asks for high accuracy first and retries with
 *      enableHighAccuracy:false on failure. Some devices never satisfy the
 *      first request.
 *
 * And the thing that will cost you an hour if nobody warns you: getUserMedia
 * and the Geolocation API only exist in a secure context. Over plain HTTP
 * navigator.mediaDevices is undefined — not blocked, undefined — so the
 * failure arrives as a TypeError that reads exactly like your own bug.
 * localhost counts as secure. http://<server-ip> does not.
 */
import Stub from '../Stub'

export default function MarkAttendance() {
  return (
    <Stub
      screen="Mark attendance"
      track="FE"
      owner="BALAJI"
      file="src/app/components/employee/MarkAttendance.tsx"
      todo={[
        'Open the camera, show a live preview, capture a frame to canvas.',
        'Keep both artefacts: a dataURL for the preview, a File for the upload.',
        'Read the current position; show accuracy in metres and let them recapture.',
        'POST /api/attendance/mark/ as multipart. Handle 409 — already marked today.',
        'Design the failure states: permission denied, no GPS fix, offline, outside class hours.',
      ]}
    />
  )
}
