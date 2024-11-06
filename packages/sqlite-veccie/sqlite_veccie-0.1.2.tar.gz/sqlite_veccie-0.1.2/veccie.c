/**
 * An sqlite extension which adds functions which can compute simple distance
 * metrics on vectors packed into BLOBs.
 *
 * Adds the following functions:
 *
 * * dot_f32(a, b) -> a . b
 * * sqdist_f32(a, b) -> sum((a - b)^2)
 *
 * Where 'a' and 'b' are each BLOBs containing a vector of 32-bit IEEE floating
 * point numbers in the system's native byte ordering. A native sqlite double
 * precision float is returned.
 */

#include <stddef.h>

#include <sqlite3ext.h> /* Do not use <sqlite3.h>! */
SQLITE_EXTENSION_INIT1

#ifdef _WIN32
__declspec(dllexport)
#endif


/* Dot product: a . b. */
float dot(const float *a, const float *b, size_t ndim) {
  float sum = 0.0f;
  for (size_t dim = 0; dim < ndim; dim++) {
    sum += a[dim] * b[dim];
  }
  return sum;
}

/* Squared distance: sum((a - b)^2) */
float sqdist(const float *a, const float *b, size_t ndim) {
  float sum = 0.0f;
  for (size_t dim = 0; dim < ndim; dim++) {
    float delta = a[dim] - b[dim];
    sum += delta * delta;
  }
  return sum;
}

/**
 * Implements (all the value checking boilerplate) for one of the *_f32
 * distance functions.
 *
 * The function to implement should be set via the 'pApp' argument to
 * sqlite3_create_function*.
 */
void func_f32(sqlite3_context *context, int argc, sqlite3_value **argv) {
  // Sanity check
  if (argc != 2) {
    sqlite3_result_error(context, "*_f32 expects exactly 2 arguments", -1);
    return;
  }
  
  // Type check
  if (
    sqlite3_value_type(argv[0]) != SQLITE_BLOB ||
    sqlite3_value_type(argv[1]) != SQLITE_BLOB
  ) {
    sqlite3_result_error(context, "*_f32 arguments must be blobs", -1);
    return;
  }
  
  // Size check
  size_t a_bytes = sqlite3_value_bytes(argv[0]);
  size_t b_bytes = sqlite3_value_bytes(argv[1]);
  if (a_bytes != b_bytes) {
    sqlite3_result_error(context, "*_f32 arguments must be same size", -1);
    return;
  }
  if (a_bytes % sizeof(float) != 0) {
    sqlite3_result_error(context, "*_f32 arguments must contain whole number of values", -1);
    return;
  }
  
  const float *a = sqlite3_value_blob(argv[0]);
  const float *b = sqlite3_value_blob(argv[1]);
  
  const float (*func)(const float *, const float *, size_t) = sqlite3_user_data(context);
  
  float result = func(a, b, a_bytes / sizeof(float));
  
  sqlite3_result_double(context, (double)result);
}

int sqlite3_veccie_init(sqlite3 *db, char **pzErrMsg, const sqlite3_api_routines *pApi) {
  SQLITE_EXTENSION_INIT2(pApi);
  
  int rc = SQLITE_OK;
  if (rc == SQLITE_OK) {
    rc = sqlite3_create_function(
      db,
      "dot_f32",
      2,
      SQLITE_UTF8 | SQLITE_DETERMINISTIC,
      dot, // pApp
      func_f32, // xFunc
      NULL, // xStep
      NULL // xFinal
    );
  }
  if (rc == SQLITE_OK) {
    rc = sqlite3_create_function(
      db,
      "sqdist_f32",
      2,
      SQLITE_UTF8 | SQLITE_DETERMINISTIC,
      sqdist, //void *pApp
      func_f32, //void (*xFunc)(sqlite3_context*,int,sqlite3_value**),
      NULL, //void (*xStep)(sqlite3_context*,int,sqlite3_value**),
      NULL //void (*xFinal)(sqlite3_context*),
    );
  }
  
  return rc;
}
