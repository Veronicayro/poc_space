# dms-adapter-api — Document Management System Adapter

**Layer:** Support | **External System:** Document Management System (DMS)

## Overview

Adaptador que abstrae la integración con el DMS externo para gestión documental del expediente crediticio. Implementa fallback local si el DMS no está disponible.

## Endpoints

| Método | Path | Descripción |
|--------|------|-------------|
| POST | `/v1/documents` | Almacenar documento (base64) |
| GET | `/v1/documents/{documentId}` | Recuperar por ID DMS |
| GET | `/v1/documents?creditRequestId={id}` | Listar por solicitud |
| DELETE | `/v1/documents/{documentId}` | Eliminar documento |

## Fallback

Si el DMS no está disponible:
1. Los documentos se almacenan temporalmente en filesystem local
2. Se marcan con flag `pending_dms_sync: true`
3. Un proceso de sincronización los envía al DMS cuando se recupere

## NFR

- Upload SLA: < 5000ms | Retrieve SLA: < 2000ms
- Max file size: 20MB | Formatos: PDF, JPG, PNG, DOCX
- Retención: 7 años mínimo (compliance crediticio)
