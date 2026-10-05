# RoomBook – business requirements

RoomBook lets university staff and students book seminar rooms.

| ID | Requirement |
|----|-------------|
| R1 | A booking has a room, a title, a start and an end. The end must be after the start, the start must be in the future and a booking may last at most 3 hours. |
| R2 | Bookings of the same room must not overlap. Intervals are half-open `[start, end)`: a booking ending at 10:00 does not conflict with one starting at 10:00. |
| R3 | All times are stored and exchanged in UTC, as ISO 8601 strings with a `Z` suffix (e.g. `2026-11-05T09:00:00Z`). |
| R4 | A booking can be cancelled only by its owner or by an administrator. |
| R5 | An owner can cancel a booking no later than 2 hours before it starts. An administrator can cancel any booking that has not started yet. |
| R6 | Personal data (e.g. the owner's e-mail address) is visible only to the owner and to administrators. Public endpoints must not expose it. |
| R7 | When a booking is cancelled, its owner receives an e-mail notification. If the notification cannot be sent, the failure is logged at ERROR level; the cancellation itself still succeeds. |
| R8 | `GET /rooms/free?start=…&end=…[&building=…]` returns the rooms that have no booking overlapping `[start, end)`, using the same overlap rule as R2. |
| R9 | Secrets (passwords, API keys, tokens) are never stored in the repository. They are provided through environment variables. |
