// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: tensorflow/compiler/mlir/tools/kernel_gen/compile_cache_item.proto

#ifndef GOOGLE_PROTOBUF_INCLUDED_tensorflow_2fcompiler_2fmlir_2ftools_2fkernel_5fgen_2fcompile_5fcache_5fitem_2eproto
#define GOOGLE_PROTOBUF_INCLUDED_tensorflow_2fcompiler_2fmlir_2ftools_2fkernel_5fgen_2fcompile_5fcache_5fitem_2eproto

#include <limits>
#include <string>

#include <google/protobuf/port_def.inc>
#if PROTOBUF_VERSION < 3021000
#error This file was generated by a newer version of protoc which is
#error incompatible with your Protocol Buffer headers. Please update
#error your headers.
#endif
#if 3021009 < PROTOBUF_MIN_PROTOC_VERSION
#error This file was generated by an older version of protoc which is
#error incompatible with your Protocol Buffer headers. Please
#error regenerate this file with a newer version of protoc.
#endif

#include <google/protobuf/port_undef.inc>
#include <google/protobuf/io/coded_stream.h>
#include <google/protobuf/arena.h>
#include <google/protobuf/arenastring.h>
#include <google/protobuf/generated_message_util.h>
#include <google/protobuf/metadata_lite.h>
#include <google/protobuf/generated_message_reflection.h>
#include <google/protobuf/message.h>
#include <google/protobuf/repeated_field.h>  // IWYU pragma: export
#include <google/protobuf/extension_set.h>  // IWYU pragma: export
#include <google/protobuf/unknown_field_set.h>
// @@protoc_insertion_point(includes)
#include <google/protobuf/port_def.inc>
#define PROTOBUF_INTERNAL_EXPORT_tensorflow_2fcompiler_2fmlir_2ftools_2fkernel_5fgen_2fcompile_5fcache_5fitem_2eproto PROTOBUF_EXPORT
PROTOBUF_NAMESPACE_OPEN
namespace internal {
class AnyMetadata;
}  // namespace internal
PROTOBUF_NAMESPACE_CLOSE

// Internal implementation detail -- do not use these members.
struct PROTOBUF_EXPORT TableStruct_tensorflow_2fcompiler_2fmlir_2ftools_2fkernel_5fgen_2fcompile_5fcache_5fitem_2eproto {
  static const uint32_t offsets[];
};
PROTOBUF_EXPORT extern const ::PROTOBUF_NAMESPACE_ID::internal::DescriptorTable descriptor_table_tensorflow_2fcompiler_2fmlir_2ftools_2fkernel_5fgen_2fcompile_5fcache_5fitem_2eproto;
namespace mlir {
namespace kernel_gen {
class CompilationCacheItem;
struct CompilationCacheItemDefaultTypeInternal;
PROTOBUF_EXPORT extern CompilationCacheItemDefaultTypeInternal _CompilationCacheItem_default_instance_;
}  // namespace kernel_gen
}  // namespace mlir
PROTOBUF_NAMESPACE_OPEN
template<> PROTOBUF_EXPORT ::mlir::kernel_gen::CompilationCacheItem* Arena::CreateMaybeMessage<::mlir::kernel_gen::CompilationCacheItem>(Arena*);
PROTOBUF_NAMESPACE_CLOSE
namespace mlir {
namespace kernel_gen {

// ===================================================================

class PROTOBUF_EXPORT CompilationCacheItem final :
    public ::PROTOBUF_NAMESPACE_ID::Message /* @@protoc_insertion_point(class_definition:mlir.kernel_gen.CompilationCacheItem) */ {
 public:
  inline CompilationCacheItem() : CompilationCacheItem(nullptr) {}
  ~CompilationCacheItem() override;
  explicit PROTOBUF_CONSTEXPR CompilationCacheItem(::PROTOBUF_NAMESPACE_ID::internal::ConstantInitialized);

  CompilationCacheItem(const CompilationCacheItem& from);
  CompilationCacheItem(CompilationCacheItem&& from) noexcept
    : CompilationCacheItem() {
    *this = ::std::move(from);
  }

  inline CompilationCacheItem& operator=(const CompilationCacheItem& from) {
    CopyFrom(from);
    return *this;
  }
  inline CompilationCacheItem& operator=(CompilationCacheItem&& from) noexcept {
    if (this == &from) return *this;
    if (GetOwningArena() == from.GetOwningArena()
  #ifdef PROTOBUF_FORCE_COPY_IN_MOVE
        && GetOwningArena() != nullptr
  #endif  // !PROTOBUF_FORCE_COPY_IN_MOVE
    ) {
      InternalSwap(&from);
    } else {
      CopyFrom(from);
    }
    return *this;
  }

  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* descriptor() {
    return GetDescriptor();
  }
  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* GetDescriptor() {
    return default_instance().GetMetadata().descriptor;
  }
  static const ::PROTOBUF_NAMESPACE_ID::Reflection* GetReflection() {
    return default_instance().GetMetadata().reflection;
  }
  static const CompilationCacheItem& default_instance() {
    return *internal_default_instance();
  }
  static inline const CompilationCacheItem* internal_default_instance() {
    return reinterpret_cast<const CompilationCacheItem*>(
               &_CompilationCacheItem_default_instance_);
  }
  static constexpr int kIndexInFileMessages =
    0;

  friend void swap(CompilationCacheItem& a, CompilationCacheItem& b) {
    a.Swap(&b);
  }
  inline void Swap(CompilationCacheItem* other) {
    if (other == this) return;
  #ifdef PROTOBUF_FORCE_COPY_IN_SWAP
    if (GetOwningArena() != nullptr &&
        GetOwningArena() == other->GetOwningArena()) {
   #else  // PROTOBUF_FORCE_COPY_IN_SWAP
    if (GetOwningArena() == other->GetOwningArena()) {
  #endif  // !PROTOBUF_FORCE_COPY_IN_SWAP
      InternalSwap(other);
    } else {
      ::PROTOBUF_NAMESPACE_ID::internal::GenericSwap(this, other);
    }
  }
  void UnsafeArenaSwap(CompilationCacheItem* other) {
    if (other == this) return;
    GOOGLE_DCHECK(GetOwningArena() == other->GetOwningArena());
    InternalSwap(other);
  }

  // implements Message ----------------------------------------------

  CompilationCacheItem* New(::PROTOBUF_NAMESPACE_ID::Arena* arena = nullptr) const final {
    return CreateMaybeMessage<CompilationCacheItem>(arena);
  }
  using ::PROTOBUF_NAMESPACE_ID::Message::CopyFrom;
  void CopyFrom(const CompilationCacheItem& from);
  using ::PROTOBUF_NAMESPACE_ID::Message::MergeFrom;
  void MergeFrom( const CompilationCacheItem& from) {
    CompilationCacheItem::MergeImpl(*this, from);
  }
  private:
  static void MergeImpl(::PROTOBUF_NAMESPACE_ID::Message& to_msg, const ::PROTOBUF_NAMESPACE_ID::Message& from_msg);
  public:
  PROTOBUF_ATTRIBUTE_REINITIALIZES void Clear() final;
  bool IsInitialized() const final;

  size_t ByteSizeLong() const final;
  const char* _InternalParse(const char* ptr, ::PROTOBUF_NAMESPACE_ID::internal::ParseContext* ctx) final;
  uint8_t* _InternalSerialize(
      uint8_t* target, ::PROTOBUF_NAMESPACE_ID::io::EpsCopyOutputStream* stream) const final;
  int GetCachedSize() const final { return _impl_._cached_size_.Get(); }

  private:
  void SharedCtor(::PROTOBUF_NAMESPACE_ID::Arena* arena, bool is_message_owned);
  void SharedDtor();
  void SetCachedSize(int size) const final;
  void InternalSwap(CompilationCacheItem* other);

  private:
  friend class ::PROTOBUF_NAMESPACE_ID::internal::AnyMetadata;
  static ::PROTOBUF_NAMESPACE_ID::StringPiece FullMessageName() {
    return "mlir.kernel_gen.CompilationCacheItem";
  }
  protected:
  explicit CompilationCacheItem(::PROTOBUF_NAMESPACE_ID::Arena* arena,
                       bool is_message_owned = false);
  public:

  static const ClassData _class_data_;
  const ::PROTOBUF_NAMESPACE_ID::Message::ClassData*GetClassData() const final;

  ::PROTOBUF_NAMESPACE_ID::Metadata GetMetadata() const final;

  // nested types ----------------------------------------------------

  // accessors -------------------------------------------------------

  enum : int {
    kOriginalModuleFieldNumber = 1,
    kResultModuleFieldNumber = 2,
  };
  // string original_module = 1;
  void clear_original_module();
  const std::string& original_module() const;
  template <typename ArgT0 = const std::string&, typename... ArgT>
  void set_original_module(ArgT0&& arg0, ArgT... args);
  std::string* mutable_original_module();
  PROTOBUF_NODISCARD std::string* release_original_module();
  void set_allocated_original_module(std::string* original_module);
  private:
  const std::string& _internal_original_module() const;
  inline PROTOBUF_ALWAYS_INLINE void _internal_set_original_module(const std::string& value);
  std::string* _internal_mutable_original_module();
  public:

  // string result_module = 2;
  void clear_result_module();
  const std::string& result_module() const;
  template <typename ArgT0 = const std::string&, typename... ArgT>
  void set_result_module(ArgT0&& arg0, ArgT... args);
  std::string* mutable_result_module();
  PROTOBUF_NODISCARD std::string* release_result_module();
  void set_allocated_result_module(std::string* result_module);
  private:
  const std::string& _internal_result_module() const;
  inline PROTOBUF_ALWAYS_INLINE void _internal_set_result_module(const std::string& value);
  std::string* _internal_mutable_result_module();
  public:

  // @@protoc_insertion_point(class_scope:mlir.kernel_gen.CompilationCacheItem)
 private:
  class _Internal;

  template <typename T> friend class ::PROTOBUF_NAMESPACE_ID::Arena::InternalHelper;
  typedef void InternalArenaConstructable_;
  typedef void DestructorSkippable_;
  struct Impl_ {
    ::PROTOBUF_NAMESPACE_ID::internal::ArenaStringPtr original_module_;
    ::PROTOBUF_NAMESPACE_ID::internal::ArenaStringPtr result_module_;
    mutable ::PROTOBUF_NAMESPACE_ID::internal::CachedSize _cached_size_;
  };
  union { Impl_ _impl_; };
  friend struct ::TableStruct_tensorflow_2fcompiler_2fmlir_2ftools_2fkernel_5fgen_2fcompile_5fcache_5fitem_2eproto;
};
// ===================================================================


// ===================================================================

#ifdef __GNUC__
  #pragma GCC diagnostic push
  #pragma GCC diagnostic ignored "-Wstrict-aliasing"
#endif  // __GNUC__
// CompilationCacheItem

// string original_module = 1;
inline void CompilationCacheItem::clear_original_module() {
  _impl_.original_module_.ClearToEmpty();
}
inline const std::string& CompilationCacheItem::original_module() const {
  // @@protoc_insertion_point(field_get:mlir.kernel_gen.CompilationCacheItem.original_module)
  return _internal_original_module();
}
template <typename ArgT0, typename... ArgT>
inline PROTOBUF_ALWAYS_INLINE
void CompilationCacheItem::set_original_module(ArgT0&& arg0, ArgT... args) {
 
 _impl_.original_module_.Set(static_cast<ArgT0 &&>(arg0), args..., GetArenaForAllocation());
  // @@protoc_insertion_point(field_set:mlir.kernel_gen.CompilationCacheItem.original_module)
}
inline std::string* CompilationCacheItem::mutable_original_module() {
  std::string* _s = _internal_mutable_original_module();
  // @@protoc_insertion_point(field_mutable:mlir.kernel_gen.CompilationCacheItem.original_module)
  return _s;
}
inline const std::string& CompilationCacheItem::_internal_original_module() const {
  return _impl_.original_module_.Get();
}
inline void CompilationCacheItem::_internal_set_original_module(const std::string& value) {
  
  _impl_.original_module_.Set(value, GetArenaForAllocation());
}
inline std::string* CompilationCacheItem::_internal_mutable_original_module() {
  
  return _impl_.original_module_.Mutable(GetArenaForAllocation());
}
inline std::string* CompilationCacheItem::release_original_module() {
  // @@protoc_insertion_point(field_release:mlir.kernel_gen.CompilationCacheItem.original_module)
  return _impl_.original_module_.Release();
}
inline void CompilationCacheItem::set_allocated_original_module(std::string* original_module) {
  if (original_module != nullptr) {
    
  } else {
    
  }
  _impl_.original_module_.SetAllocated(original_module, GetArenaForAllocation());
#ifdef PROTOBUF_FORCE_COPY_DEFAULT_STRING
  if (_impl_.original_module_.IsDefault()) {
    _impl_.original_module_.Set("", GetArenaForAllocation());
  }
#endif // PROTOBUF_FORCE_COPY_DEFAULT_STRING
  // @@protoc_insertion_point(field_set_allocated:mlir.kernel_gen.CompilationCacheItem.original_module)
}

// string result_module = 2;
inline void CompilationCacheItem::clear_result_module() {
  _impl_.result_module_.ClearToEmpty();
}
inline const std::string& CompilationCacheItem::result_module() const {
  // @@protoc_insertion_point(field_get:mlir.kernel_gen.CompilationCacheItem.result_module)
  return _internal_result_module();
}
template <typename ArgT0, typename... ArgT>
inline PROTOBUF_ALWAYS_INLINE
void CompilationCacheItem::set_result_module(ArgT0&& arg0, ArgT... args) {
 
 _impl_.result_module_.Set(static_cast<ArgT0 &&>(arg0), args..., GetArenaForAllocation());
  // @@protoc_insertion_point(field_set:mlir.kernel_gen.CompilationCacheItem.result_module)
}
inline std::string* CompilationCacheItem::mutable_result_module() {
  std::string* _s = _internal_mutable_result_module();
  // @@protoc_insertion_point(field_mutable:mlir.kernel_gen.CompilationCacheItem.result_module)
  return _s;
}
inline const std::string& CompilationCacheItem::_internal_result_module() const {
  return _impl_.result_module_.Get();
}
inline void CompilationCacheItem::_internal_set_result_module(const std::string& value) {
  
  _impl_.result_module_.Set(value, GetArenaForAllocation());
}
inline std::string* CompilationCacheItem::_internal_mutable_result_module() {
  
  return _impl_.result_module_.Mutable(GetArenaForAllocation());
}
inline std::string* CompilationCacheItem::release_result_module() {
  // @@protoc_insertion_point(field_release:mlir.kernel_gen.CompilationCacheItem.result_module)
  return _impl_.result_module_.Release();
}
inline void CompilationCacheItem::set_allocated_result_module(std::string* result_module) {
  if (result_module != nullptr) {
    
  } else {
    
  }
  _impl_.result_module_.SetAllocated(result_module, GetArenaForAllocation());
#ifdef PROTOBUF_FORCE_COPY_DEFAULT_STRING
  if (_impl_.result_module_.IsDefault()) {
    _impl_.result_module_.Set("", GetArenaForAllocation());
  }
#endif // PROTOBUF_FORCE_COPY_DEFAULT_STRING
  // @@protoc_insertion_point(field_set_allocated:mlir.kernel_gen.CompilationCacheItem.result_module)
}

#ifdef __GNUC__
  #pragma GCC diagnostic pop
#endif  // __GNUC__

// @@protoc_insertion_point(namespace_scope)

}  // namespace kernel_gen
}  // namespace mlir

// @@protoc_insertion_point(global_scope)

#include <google/protobuf/port_undef.inc>
#endif  // GOOGLE_PROTOBUF_INCLUDED_GOOGLE_PROTOBUF_INCLUDED_tensorflow_2fcompiler_2fmlir_2ftools_2fkernel_5fgen_2fcompile_5fcache_5fitem_2eproto
