const PYTHON_SERVER_URL = "http://localhost:5001/status";
const CHECK_ALARM_NAME = "checkDistractionStatusAlarm";
const CHECK_INTERVAL_MINUTES = 0.02;

const NORMAL_ICON_PATHS = {
    "16": "icons/icon_normal_16.png",
    "48": "icons/icon_normal_48.png"
};
const ALERT_ICON_PATHS = {
    "16": "icons/icon_alert_16.png",
    "48": "icons/icon_alert_48.png"
};

const BLINK_INTERVAL_MS = 300;
const BLINK_DURATION_MS = 2100;

let isBlinking = false;
let blinkTimeoutId = null;
let blinkIntervalTimerId = null;
let iconIsAlertStateForBlink = false;

function setIcon(iconPaths) {
  chrome.action.setIcon({ path: iconPaths }, () => {
		if (chrome.runtime.lastError) {
			console.error("setIcon Error directly in callback:", chrome.runtime.lastError.message, "Paths used:", iconPaths);
		}
	});
}

function startBlinkingEffect() {
	if (isBlinking) {
		clearTimeout(blinkTimeoutId);
	} else {
		isBlinking = true;
		iconIsAlertStateForBlink = true;
		setIcon(ALERT_ICON_PATHS);
	}

	if (blinkIntervalTimerId) {
		clearInterval(blinkIntervalTimerId);
	}

	blinkIntervalTimerId = setInterval(() => {
		iconIsAlertStateForBlink = !iconIsAlertStateForBlink;
		setIcon(iconIsAlertStateForBlink ? ALERT_ICON_PATHS : NORMAL_ICON_PATHS);
	}, BLINK_INTERVAL_MS);

	blinkTimeoutId = setTimeout(() => {
		stopBlinkingEffect(true);
	}, BLINK_DURATION_MS);
}

function stopBlinkingEffect(stillDistractedAfterBlinkCycle = false) {
	clearInterval(blinkIntervalTimerId);
	clearTimeout(blinkTimeoutId);
	blinkIntervalTimerId = null;
	blinkTimeoutId = null;
	isBlinking = false;

	setIcon(NORMAL_ICON_PATHS);
}

// --- Status Checking Function ---
async function checkStatus() {
	console.log("Checking distraction status...");
	try {
		const response = await fetch(PYTHON_SERVER_URL);
		if (!response.ok) {
			console.error("Error fetching status from Python server:", response.status, response.statusText);
			if (isBlinking) stopBlinkingEffect(false);
			setIcon(NORMAL_ICON_PATHS);
			return;
		}
		const data = await response.json();
		console.log("Status received:", data);

		if (data.distracted) {
			startBlinkingEffect();
		} else {
			if (isBlinking) {
				stopBlinkingEffect(false);
			}
			setIcon(NORMAL_ICON_PATHS);
		}
	} catch (error) {
		console.error("failed to fetch or parse status:", error);
		if (isBlinking) stopBlinkingEffect(false);
		setIcon(NORMAL_ICON_PATHS);
	}
}

// --- Alarm Setup ---
console.log("Attempting to add alarm listener. chrome.alarms is:", chrome.alarms);
// Listerner for when the alarm goes off
chrome.alarms.onAlarm.addListener((alarm) => {
	if (alarm.name === CHECK_ALARM_NAME) {
		checkStatus();
	}
});

function setupAlarm() {
	chrome.alarms.get(CHECK_ALARM_NAME, (alarm) => {
		if (alarm) {
			console.log("Alarm already exists.");
		} else {
			chrome.alarms.create(CHECK_ALARM_NAME, {
				delayInMinutes: 0.1,
				periodInMinutes: CHECK_INTERVAL_MINUTES
			});
			console.log("Alarm created.");
		}
	});
}

// --- Extension Lifecycle events ---
chrome.runtime.onInstalled.addListener(() => {
	console.log(NORMAL_ICON_PATHS);
	setIcon(NORMAL_ICON_PATHS);
	setupAlarm();
	checkStatus();
});

chrome.runtime.onStartup.addListener(() => {
	console.log("Distraction Detector extension started with Chrome.");
	setIcon(NORMAL_ICON_PATHS);
	setupAlarm();
	checkStatus();
});

console.log("Background service worker started/restarted.");
setIcon(NORMAL_ICON_PATHS);
setupAlarm();
checkStatus();