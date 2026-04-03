const rawEvents = Array.isArray(window.ME_CALENDAR_EVENTS)
  ? window.ME_CALENDAR_EVENTS
  : [];
const meta = window.ME_CALENDAR_DATA_META || {};

const statusEl = document.getElementById("status");
const listEl = document.getElementById("monthEventList");
const summaryTitle = document.getElementById("summaryTitle");
const rangeLabel = document.getElementById("rangeLabel");
const viewButtons = Array.from(document.querySelectorAll(".view-btn"));

const Calendar = window.tui && window.tui.Calendar ? window.tui.Calendar : null;
const MOBILE_QUERY = window.matchMedia("(max-width: 768px)");

function pad(num) {
  return String(num).padStart(2, "0");
}

function formatYMD(date) {
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}`;
}

function escapeHtml(text) {
  return String(text)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

function getRange(view, baseDate) {
  const year = baseDate.getFullYear();
  const month = baseDate.getMonth();
  let start;
  let end;

  if (view === "month") {
    start = new Date(year, month, 1);
    end = new Date(year, month + 1, 0);
  } else if (view === "week") {
    const dayIndex = (baseDate.getDay() + 6) % 7; // Monday = 0
    start = new Date(year, month, baseDate.getDate() - dayIndex);
    end = new Date(start.getFullYear(), start.getMonth(), start.getDate() + 6);
  } else {
    start = new Date(year, month, baseDate.getDate());
    end = new Date(year, month, baseDate.getDate());
  }

  start.setHours(0, 0, 0, 0);
  end.setHours(23, 59, 59, 999);
  return { start, end };
}

function toToastEvent(item) {
  const isMonthOnly = Boolean(item.month_only);
  const calendarId = isMonthOnly ? "month-only" : item.done ? "done" : "todo";
  const titlePrefix = isMonthOnly ? "[月任务] " : "";
  const tags = Array.isArray(item.tags) ? item.tags : [];
  return {
    id: item.id,
    calendarId,
    title: `${titlePrefix}${item.title}`,
    start: item.date,
    end: item.date,
    isAllday: true,
    category: "allday",
    isReadOnly: true,
    raw: {
      source: item.source || "",
      monthOnly: isMonthOnly,
      done: Boolean(item.done),
      tags,
    },
  };
}

if (!Calendar) {
  if (statusEl) {
    statusEl.textContent = "Calendar 库未加载，请检查 toastui-calendar 资源是否可访问。";
  }
} else {
  const dayNames = ["日", "一", "二", "三", "四", "五", "六"];
  const calendars = [
    {
      id: "done",
      name: "完成",
      backgroundColor: "#16a34a",
      borderColor: "#16a34a",
      color: "#ffffff",
    },
    {
      id: "todo",
      name: "待完成",
      backgroundColor: "#f59e0b",
      borderColor: "#f59e0b",
      color: "#1a2220",
    },
    {
      id: "month-only",
      name: "月任务",
      backgroundColor: "#c4b5fd",
      borderColor: "#a78bfa",
      color: "#1a2220",
    },
  ];

  let currentView = "month";
  let currentDate = new Date();

  function buildOptions(isMobile) {
    return {
      week: {
        startDayOfWeek: 1,
        dayNames,
        narrowWeekend: false,
        showNowIndicator: !isMobile,
        taskView: false,
        eventView: isMobile ? ["allday"] : true,
      },
      month: {
        startDayOfWeek: 1,
        dayNames,
        narrowWeekend: false,
        isAlways6Weeks: !isMobile,
        visibleEventCount: isMobile ? 4 : 5,
      },
    };
  }

  const responsiveOptions = buildOptions(MOBILE_QUERY.matches);

  const calendar = new Calendar("#toastCalendar", {
    defaultView: currentView,
    isReadOnly: true,
    useDetailPopup: true,
    useFormPopup: false,
    usageStatistics: false,
    template: {
      popupDetailTitle({ title, raw }) {
        const tags = raw && Array.isArray(raw.tags) ? raw.tags : [];
        if (!tags.length) return escapeHtml(title);
        const safeTags = tags.map(escapeHtml).join(" / ");
        return `${escapeHtml(title)}<div class="popup-tags-inline">标签：${safeTags}</div>`;
      },
      popupDetailBody({ raw }) {
        const tags = raw && Array.isArray(raw.tags) ? raw.tags : [];
        if (!tags.length) return "";
        const safe = tags.map(escapeHtml).join(" / ");
        return `<div class="popup-tags"><strong>标签</strong>：${safe}</div>`;
      },
    },
    calendars,
    week: responsiveOptions.week,
    month: responsiveOptions.month,
  });

  calendar.createEvents(rawEvents.map(toToastEvent));

  function updateActiveView() {
    viewButtons.forEach((btn) => {
      const view = btn.dataset.view;
      if (view === currentView) {
        btn.classList.add("active");
      } else {
        btn.classList.remove("active");
      }
    });
  }

  function updateRangeLabel() {
    if (!rangeLabel) return;
    if (currentView === "month") {
      rangeLabel.textContent = `${currentDate.getFullYear()} 年 ${pad(currentDate.getMonth() + 1)} 月`;
      return;
    }
    const range = getRange(currentView, currentDate);
    const label = currentView === "day"
      ? `${formatYMD(range.start)}`
      : `${formatYMD(range.start)} ~ ${formatYMD(range.end)}`;
    rangeLabel.textContent = label;
  }

  function updateSummaryTitle() {
    if (!summaryTitle) return;
    if (currentView === "month") summaryTitle.textContent = "当月任务清单";
    else if (currentView === "week") summaryTitle.textContent = "当周任务清单";
    else summaryTitle.textContent = "当日任务清单";
  }

  function updateSummaryList() {
    if (!listEl) return;
    const { start, end } = getRange(currentView, currentDate);
    const filtered = rawEvents
      .filter((event) => {
        const date = new Date(`${event.date}T00:00:00`);
        return date >= start && date <= end;
      })
      .sort((a, b) => (a.date < b.date ? -1 : a.date > b.date ? 1 : 0));

    if (!filtered.length) {
      listEl.innerHTML = "<li>当前范围暂无任务</li>";
      return;
    }

    listEl.innerHTML = filtered
      .map((event) => {
        const icon = event.done ? "✅" : "○";
        const dateText = event.date;
        const tag = event.month_only ? '<span class="summary-tag">月任务</span>' : "";
        const tags = Array.isArray(event.tags) && event.tags.length
          ? `<span class="summary-tag">${escapeHtml(event.tags.join("/"))}</span>`
          : "";
        const source = event.source
          ? ` <a href="${event.source}" target="_blank" rel="noopener">来源</a>`
          : "";
        const dotClass = event.month_only
          ? "summary-dot month-only"
          : event.done
          ? "summary-dot done"
          : "summary-dot todo";
        return `<li><span class="${dotClass}"></span>${icon} ${dateText} ${tag} ${tags} ${escapeHtml(event.title)}${source}</li>`;
      })
      .join("");
  }

  function updateStatus() {
    if (!statusEl) return;
    const generated = meta.generated_at || "manual";
    const count = meta.count || rawEvents.length;
    statusEl.textContent = `已加载 ${count} 条任务 | 数据生成: ${generated}`;
  }

  function refreshUI() {
    updateActiveView();
    updateRangeLabel();
    updateSummaryTitle();
    updateSummaryList();
    updateStatus();
  }

  function applyResponsiveOptions(isMobile) {
    const next = buildOptions(isMobile);
    calendar.setOptions({
      week: next.week,
      month: next.month,
    });
    refreshUI();
  }

  const prevBtn = document.getElementById("prevBtn");
  const nextBtn = document.getElementById("nextBtn");
  const todayBtn = document.getElementById("todayBtn");
  const calendarFrame = document.querySelector(".calendar-frame");
  const toolbarEl = document.querySelector(".toolbar");

  if (prevBtn) {
    prevBtn.addEventListener("click", () => {
      calendar.prev();
      if (currentView === "month") currentDate.setMonth(currentDate.getMonth() - 1);
      else if (currentView === "week") currentDate.setDate(currentDate.getDate() - 7);
      else currentDate.setDate(currentDate.getDate() - 1);
      refreshUI();
    });
  }

  if (nextBtn) {
    nextBtn.addEventListener("click", () => {
      calendar.next();
      if (currentView === "month") currentDate.setMonth(currentDate.getMonth() + 1);
      else if (currentView === "week") currentDate.setDate(currentDate.getDate() + 7);
      else currentDate.setDate(currentDate.getDate() + 1);
      refreshUI();
    });
  }

  if (todayBtn) {
    todayBtn.addEventListener("click", () => {
      calendar.today();
      currentDate = new Date();
      refreshUI();
    });
  }

  viewButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      const view = btn.dataset.view;
      if (!view || view === currentView) return;
      currentView = view;
      calendar.changeView(view);
      refreshUI();
      syncCalendarHeight();
    });
  });

  function syncCalendarHeight() {
    if (!calendarFrame) return;
    if (!MOBILE_QUERY.matches) {
      calendarFrame.style.removeProperty("height");
      calendarFrame.style.removeProperty("min-height");
      calendar.render();
      return;
    }

    const viewport = window.innerHeight || document.documentElement.clientHeight || 0;
    const toolbarHeight = toolbarEl ? toolbarEl.offsetHeight : 0;
    const target = Math.max(viewport - toolbarHeight, 320);
    calendarFrame.style.height = `${target}px`;
    calendarFrame.style.minHeight = `${target}px`;
    calendar.render();
  }

  let resizeTimer = null;
  function onResize() {
    if (resizeTimer) clearTimeout(resizeTimer);
    resizeTimer = setTimeout(syncCalendarHeight, 120);
  }

  if (typeof MOBILE_QUERY.addEventListener === "function") {
    MOBILE_QUERY.addEventListener("change", (event) => {
      applyResponsiveOptions(event.matches);
      syncCalendarHeight();
    });
  } else if (typeof MOBILE_QUERY.addListener === "function") {
    MOBILE_QUERY.addListener((event) => {
      applyResponsiveOptions(event.matches);
      syncCalendarHeight();
    });
  }

  refreshUI();
  syncCalendarHeight();
  window.addEventListener("resize", onResize);
  window.addEventListener("orientationchange", onResize);
}
