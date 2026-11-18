// Prints the reviewer split direction: "right" when the Ghostty window that
// shows the Herdr client is on a landscape screen, and "down" when it is on a
// portrait screen. It exits non-zero when it cannot find that window.
//
// Usage: osascript -l JavaScript split-direction.js [--self-check]
ObjC.import("AppKit");

// System Events measures y down from the top of the main screen, and AppKit
// measures y up from the bottom, so the check flips each screen frame.
// AppKit lists the main screen first.
function directionAt(centerX, centerY, screens) {
  const mainHeight = screens[0].height;
  const screen = screens.find((frame) => {
    const top = mainHeight - frame.y - frame.height;
    return centerX >= frame.x && centerX < frame.x + frame.width && centerY >= top && centerY < top + frame.height;
  });
  if (!screen) throw new Error("The Ghostty window is on no screen");
  return screen.width >= screen.height ? "right" : "down";
}

function selfCheck() {
  // Each point sits near a flipped top edge, so a wrong flip misses its screen.
  const screens = [
    { x: 0, y: 0, width: 1920, height: 1080 },
    { x: 0, y: 1080, width: 1920, height: 1200 },
    { x: 1920, y: -426, width: 1080, height: 1920 },
    { x: 0, y: -1920, width: 1080, height: 1920 },
  ];
  const cases = [[960, 540, "right"], [2460, -400, "down"], [540, 1100, "down"], [960, -540, "right"]];
  for (const [x, y, expected] of cases) {
    const actual = directionAt(x, y, screens);
    if (actual !== expected) throw new Error(`(${x}, ${y}): expected ${expected}, got ${actual}`);
  }
  return "self-check ok";
}

function herdrClientTtys() {
  const app = Application.currentApplication();
  app.includeStandardAdditions = true;
  const output = app.doShellScript(`ps -axo tty=,ucomm= | awk '$2 == "herdr" && $1 ~ /^ttys/ {print "/dev/" $1}'`);
  return output.split(/[\r\n]+/).filter(Boolean);
}

function screenFrames() {
  return ObjC.unwrap($.NSScreen.screens).map((screen) => {
    const frame = screen.frame;
    return { x: frame.origin.x, y: frame.origin.y, width: frame.size.width, height: frame.size.height };
  });
}

function run(argv) {
  if (argv[0] === "--self-check") return selfCheck();
  const ttys = herdrClientTtys();
  const ghostty = Application("Ghostty");
  // A query to an app that is not running launches it, so stop first.
  if (ttys.length === 0 || !ghostty.running()) throw new Error("No Herdr client runs in Ghostty");
  // ponytail: The first Ghostty window that shows a Herdr client decides, and
  // System Events finds that window by its title. Match a window id if several
  // clients or windows with one title appear on screens with different orientations.
  const index = ghostty.windows.tabs.terminals.tty().findIndex((tabs) => tabs.flat().some((tty) => ttys.includes(tty)));
  if (index < 0) throw new Error(`No Ghostty window shows a Herdr client (${ttys.join(" ")})`);
  const window = Application("System Events").processes.byName("Ghostty").windows.byName(ghostty.windows[index].name());
  const [x, y] = window.position();
  const [width, height] = window.size();
  return directionAt(x + width / 2, y + height / 2, screenFrames());
}
