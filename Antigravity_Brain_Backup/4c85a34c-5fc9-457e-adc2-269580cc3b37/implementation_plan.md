# YouTube Factory 2 Dashboard Implementation Plan

## Goal Description
Set up a dedicated dashboard for "YouTube Factory 2" in the designated folder. This dashboard will serve as the control center for the YouTube automation workflows (previously discussed as "YouTube Radio"). It will visually distinct itself as "Factory 2" and include features to monitor and control the automation process.

## User Review Required
> [!IMPORTANT]
> The current folder `c:/Upload2601공유폴더/0123 upload 유튜브만들기 2공장` is empty. I will initialize a new **Next.js** project here to serve as the dashboard.
> I will assume the "automation logic" (Python scripts, etc.) will be integrated or added later. This plan focuses on the **Dashboard UI** setup.

## Proposed Changes

### Project Initialization
- Initialize a new Next.js application (App Router) in the root of the workspace.
- Install necessary dependencies: `lucide-react` (icons), `recharts` (charts if needed), `framer-motion` (animations).
- Configure TailwindCSS for styling (using a "Factory 2" theme, perhaps distinct from Factory 1).

### Dashboard UI Structure
#### [NEW] `app/page.tsx`
- Main Dashboard view.
- **Header**: "YouTube Factory 2 Control Center"
- **Status Panel**: Current status of the factory (Idle, Running, Error).
- **Recent Activity**: Log of recent actions (e.g., "Video #101 uploaded", "Script generated").
- **Quick Actions**: Buttons to "Start Workflow", "Emergency Stop".

#### [NEW] `components/StatusCard.tsx`
- Component to display key metrics (CPU/Memory usage of factory, Queue size).

#### [NEW] `components/WorkflowVisualizer.tsx`
- Visual representation of the pipeline (Topic -> Script -> Audio -> Video -> Upload).

## Verification Plan

### Automated Tests
- Run `npm run build` to ensure the project builds successfully.
- Run `npm run lint` to check for coding standards.

### Manual Verification
- Start the dev server (`npm run dev`).
- Open the dashboard in the browser.
- Verify the "Factory 2" branding is visible.
- Check responsiveness and basic interactivity of the UI components.
