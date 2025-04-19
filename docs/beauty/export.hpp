
#ifndef BEAUTY_EXPORT_H
#define BEAUTY_EXPORT_H

#ifdef BEAUTY_STATIC_DEFINE
#  define BEAUTY_EXPORT
#  define BEAUTY_NO_EXPORT
#else
#  ifndef BEAUTY_EXPORT
#    ifdef beauty_EXPORTS
        /* We are building this library */
#      define BEAUTY_EXPORT 
#    else
        /* We are using this library */
#      define BEAUTY_EXPORT 
#    endif
#  endif

#  ifndef BEAUTY_NO_EXPORT
#    define BEAUTY_NO_EXPORT 
#  endif
#endif

#ifndef BEAUTY_DEPRECATED
#  define BEAUTY_DEPRECATED __attribute__ ((__deprecated__))
#endif

#ifndef BEAUTY_DEPRECATED_EXPORT
#  define BEAUTY_DEPRECATED_EXPORT BEAUTY_EXPORT BEAUTY_DEPRECATED
#endif

#ifndef BEAUTY_DEPRECATED_NO_EXPORT
#  define BEAUTY_DEPRECATED_NO_EXPORT BEAUTY_NO_EXPORT BEAUTY_DEPRECATED
#endif

/* NOLINTNEXTLINE(readability-avoid-unconditional-preprocessor-if) */
#if 0 /* DEFINE_NO_DEPRECATED */
#  ifndef BEAUTY_NO_DEPRECATED
#    define BEAUTY_NO_DEPRECATED
#  endif
#endif

#endif /* BEAUTY_EXPORT_H */
