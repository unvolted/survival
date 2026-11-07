// ROOTFALL log categories.

#pragma once

#include "CoreMinimal.h"

/** General ROOTFALL gameplay log. */
ROOTFALL_API DECLARE_LOG_CATEGORY_EXTERN(LogRF, Log, All);

/** Debug console commands and debug flags (RF_* commands, rf.* CVars). */
ROOTFALL_API DECLARE_LOG_CATEGORY_EXTERN(LogRFDebug, Log, All);
