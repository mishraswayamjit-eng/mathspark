/**
 * Lightweight runtime validation for API request bodies.
 * Checks that required fields exist and have the expected type.
 */

type FieldType = 'string' | 'number' | 'boolean' | 'object'
  | 'string?' | 'number?' | 'boolean?' | 'object?' | 'array?' | 'array';

export class ValidationError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'ValidationError';
  }
}

export function validateBody<T extends Record<string, unknown>>(
  body: unknown,
  schema: Record<string, FieldType>,
): T {
  if (!body || typeof body !== 'object' || Array.isArray(body)) {
    throw new ValidationError('Request body must be a JSON object');
  }

  const obj = body as Record<string, unknown>;

  for (const [key, spec] of Object.entries(schema)) {
    const optional = spec.endsWith('?');
    const baseType = optional ? spec.slice(0, -1) : spec;
    const value = obj[key];

    if (value === undefined || value === null) {
      if (!optional) throw new ValidationError(`Missing required field: ${key}`);
      continue;
    }

    if (baseType === 'array') {
      if (!Array.isArray(value)) throw new ValidationError(`Field "${key}" must be an array`);
    } else if (typeof value !== baseType) {
      throw new ValidationError(`Field "${key}" must be a ${baseType}, got ${typeof value}`);
    }
  }

  return obj as T;
}
