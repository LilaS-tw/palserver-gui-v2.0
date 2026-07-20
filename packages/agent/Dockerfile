# Builds the palserver agent (with the web UI bundled) into a single image.
FROM node:22-bookworm-slim AS build
RUN corepack enable \
    && apt-get update \
    && apt-get install -y --no-install-recommends python3 python3-pip python3-venv libfontconfig1 libgl1 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
ENV CI=true
COPY . .
RUN pnpm install --frozen-lockfile \
    && pnpm -r build \
    && python3 -m venv /tmp/renderer-venv \
    && /tmp/renderer-venv/bin/pip install -r scripts/message-card-renderer-requirements.txt pyinstaller==6.21.0 \
    && /tmp/renderer-venv/bin/pyinstaller --clean --onedir --name bridge-card-renderer --exclude-module cv2 --exclude-module numpy --exclude-module pil_utils.build_image --exclude-module pil_utils.gradient scripts/message-card-renderer.py

FROM node:22-bookworm-slim
RUN corepack enable \
    && apt-get update \
    && apt-get install -y --no-install-recommends libfontconfig1 libgl1 fonts-noto-cjk \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY --from=build /app/package.json /app/pnpm-workspace.yaml /app/pnpm-lock.yaml ./
COPY --from=build /app/packages/shared/package.json packages/shared/
COPY --from=build /app/packages/shared/dist packages/shared/dist
COPY --from=build /app/packages/agent/package.json packages/agent/
COPY --from=build /app/packages/agent/dist packages/agent/dist
COPY --from=build /app/packages/web/dist packages/web/dist
COPY --from=build /app/dist/bridge-card-renderer /app/bridge-card-renderer
COPY --from=build /app/THIRD_PARTY_LICENSES.md /app/THIRD_PARTY_LICENSES.md
RUN pnpm install --frozen-lockfile --prod --filter @palserver/agent --filter @palserver/shared
ENV PALSERVER_MESSAGE_RENDERER=/app/bridge-card-renderer/bridge-card-renderer
EXPOSE 8250
CMD ["node", "packages/agent/dist/index.js"]
