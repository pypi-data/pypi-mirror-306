// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: xla/pjrt/stream_executor_executable.proto

#ifndef GOOGLE_PROTOBUF_INCLUDED_xla_2fpjrt_2fstream_5fexecutor_5fexecutable_2eproto
#define GOOGLE_PROTOBUF_INCLUDED_xla_2fpjrt_2fstream_5fexecutor_5fexecutable_2eproto

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
#include "xla/pjrt/compile_options.pb.h"
// @@protoc_insertion_point(includes)
#include <google/protobuf/port_def.inc>
#define PROTOBUF_INTERNAL_EXPORT_xla_2fpjrt_2fstream_5fexecutor_5fexecutable_2eproto PROTOBUF_EXPORT
PROTOBUF_NAMESPACE_OPEN
namespace internal {
class AnyMetadata;
}  // namespace internal
PROTOBUF_NAMESPACE_CLOSE

// Internal implementation detail -- do not use these members.
struct PROTOBUF_EXPORT TableStruct_xla_2fpjrt_2fstream_5fexecutor_5fexecutable_2eproto {
  static const uint32_t offsets[];
};
PROTOBUF_EXPORT extern const ::PROTOBUF_NAMESPACE_ID::internal::DescriptorTable descriptor_table_xla_2fpjrt_2fstream_5fexecutor_5fexecutable_2eproto;
namespace xla {
class StreamExecutorExecutableProto;
struct StreamExecutorExecutableProtoDefaultTypeInternal;
PROTOBUF_EXPORT extern StreamExecutorExecutableProtoDefaultTypeInternal _StreamExecutorExecutableProto_default_instance_;
}  // namespace xla
PROTOBUF_NAMESPACE_OPEN
template<> PROTOBUF_EXPORT ::xla::StreamExecutorExecutableProto* Arena::CreateMaybeMessage<::xla::StreamExecutorExecutableProto>(Arena*);
PROTOBUF_NAMESPACE_CLOSE
namespace xla {

// ===================================================================

class PROTOBUF_EXPORT StreamExecutorExecutableProto final :
    public ::PROTOBUF_NAMESPACE_ID::Message /* @@protoc_insertion_point(class_definition:xla.StreamExecutorExecutableProto) */ {
 public:
  inline StreamExecutorExecutableProto() : StreamExecutorExecutableProto(nullptr) {}
  ~StreamExecutorExecutableProto() override;
  explicit PROTOBUF_CONSTEXPR StreamExecutorExecutableProto(::PROTOBUF_NAMESPACE_ID::internal::ConstantInitialized);

  StreamExecutorExecutableProto(const StreamExecutorExecutableProto& from);
  StreamExecutorExecutableProto(StreamExecutorExecutableProto&& from) noexcept
    : StreamExecutorExecutableProto() {
    *this = ::std::move(from);
  }

  inline StreamExecutorExecutableProto& operator=(const StreamExecutorExecutableProto& from) {
    CopyFrom(from);
    return *this;
  }
  inline StreamExecutorExecutableProto& operator=(StreamExecutorExecutableProto&& from) noexcept {
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
  static const StreamExecutorExecutableProto& default_instance() {
    return *internal_default_instance();
  }
  static inline const StreamExecutorExecutableProto* internal_default_instance() {
    return reinterpret_cast<const StreamExecutorExecutableProto*>(
               &_StreamExecutorExecutableProto_default_instance_);
  }
  static constexpr int kIndexInFileMessages =
    0;

  friend void swap(StreamExecutorExecutableProto& a, StreamExecutorExecutableProto& b) {
    a.Swap(&b);
  }
  inline void Swap(StreamExecutorExecutableProto* other) {
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
  void UnsafeArenaSwap(StreamExecutorExecutableProto* other) {
    if (other == this) return;
    GOOGLE_DCHECK(GetOwningArena() == other->GetOwningArena());
    InternalSwap(other);
  }

  // implements Message ----------------------------------------------

  StreamExecutorExecutableProto* New(::PROTOBUF_NAMESPACE_ID::Arena* arena = nullptr) const final {
    return CreateMaybeMessage<StreamExecutorExecutableProto>(arena);
  }
  using ::PROTOBUF_NAMESPACE_ID::Message::CopyFrom;
  void CopyFrom(const StreamExecutorExecutableProto& from);
  using ::PROTOBUF_NAMESPACE_ID::Message::MergeFrom;
  void MergeFrom( const StreamExecutorExecutableProto& from) {
    StreamExecutorExecutableProto::MergeImpl(*this, from);
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
  void InternalSwap(StreamExecutorExecutableProto* other);

  private:
  friend class ::PROTOBUF_NAMESPACE_ID::internal::AnyMetadata;
  static ::PROTOBUF_NAMESPACE_ID::StringPiece FullMessageName() {
    return "xla.StreamExecutorExecutableProto";
  }
  protected:
  explicit StreamExecutorExecutableProto(::PROTOBUF_NAMESPACE_ID::Arena* arena,
                       bool is_message_owned = false);
  public:

  static const ClassData _class_data_;
  const ::PROTOBUF_NAMESPACE_ID::Message::ClassData*GetClassData() const final;

  ::PROTOBUF_NAMESPACE_ID::Metadata GetMetadata() const final;

  // nested types ----------------------------------------------------

  // accessors -------------------------------------------------------

  enum : int {
    kExecutablesFieldNumber = 2,
    kNameFieldNumber = 5,
    kFingerprintFieldNumber = 6,
    kCompileOptionsFieldNumber = 1,
    kNumReplicasFieldNumber = 3,
    kNumPartitionsFieldNumber = 4,
  };
  // repeated bytes executables = 2;
  int executables_size() const;
  private:
  int _internal_executables_size() const;
  public:
  void clear_executables();
  const std::string& executables(int index) const;
  std::string* mutable_executables(int index);
  void set_executables(int index, const std::string& value);
  void set_executables(int index, std::string&& value);
  void set_executables(int index, const char* value);
  void set_executables(int index, const void* value, size_t size);
  std::string* add_executables();
  void add_executables(const std::string& value);
  void add_executables(std::string&& value);
  void add_executables(const char* value);
  void add_executables(const void* value, size_t size);
  const ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField<std::string>& executables() const;
  ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField<std::string>* mutable_executables();
  private:
  const std::string& _internal_executables(int index) const;
  std::string* _internal_add_executables();
  public:

  // string name = 5;
  void clear_name();
  const std::string& name() const;
  template <typename ArgT0 = const std::string&, typename... ArgT>
  void set_name(ArgT0&& arg0, ArgT... args);
  std::string* mutable_name();
  PROTOBUF_NODISCARD std::string* release_name();
  void set_allocated_name(std::string* name);
  private:
  const std::string& _internal_name() const;
  inline PROTOBUF_ALWAYS_INLINE void _internal_set_name(const std::string& value);
  std::string* _internal_mutable_name();
  public:

  // string fingerprint = 6;
  void clear_fingerprint();
  const std::string& fingerprint() const;
  template <typename ArgT0 = const std::string&, typename... ArgT>
  void set_fingerprint(ArgT0&& arg0, ArgT... args);
  std::string* mutable_fingerprint();
  PROTOBUF_NODISCARD std::string* release_fingerprint();
  void set_allocated_fingerprint(std::string* fingerprint);
  private:
  const std::string& _internal_fingerprint() const;
  inline PROTOBUF_ALWAYS_INLINE void _internal_set_fingerprint(const std::string& value);
  std::string* _internal_mutable_fingerprint();
  public:

  // .xla.CompileOptionsProto compile_options = 1;
  bool has_compile_options() const;
  private:
  bool _internal_has_compile_options() const;
  public:
  void clear_compile_options();
  const ::xla::CompileOptionsProto& compile_options() const;
  PROTOBUF_NODISCARD ::xla::CompileOptionsProto* release_compile_options();
  ::xla::CompileOptionsProto* mutable_compile_options();
  void set_allocated_compile_options(::xla::CompileOptionsProto* compile_options);
  private:
  const ::xla::CompileOptionsProto& _internal_compile_options() const;
  ::xla::CompileOptionsProto* _internal_mutable_compile_options();
  public:
  void unsafe_arena_set_allocated_compile_options(
      ::xla::CompileOptionsProto* compile_options);
  ::xla::CompileOptionsProto* unsafe_arena_release_compile_options();

  // int32 num_replicas = 3;
  void clear_num_replicas();
  int32_t num_replicas() const;
  void set_num_replicas(int32_t value);
  private:
  int32_t _internal_num_replicas() const;
  void _internal_set_num_replicas(int32_t value);
  public:

  // int32 num_partitions = 4;
  void clear_num_partitions();
  int32_t num_partitions() const;
  void set_num_partitions(int32_t value);
  private:
  int32_t _internal_num_partitions() const;
  void _internal_set_num_partitions(int32_t value);
  public:

  // @@protoc_insertion_point(class_scope:xla.StreamExecutorExecutableProto)
 private:
  class _Internal;

  template <typename T> friend class ::PROTOBUF_NAMESPACE_ID::Arena::InternalHelper;
  typedef void InternalArenaConstructable_;
  typedef void DestructorSkippable_;
  struct Impl_ {
    ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField<std::string> executables_;
    ::PROTOBUF_NAMESPACE_ID::internal::ArenaStringPtr name_;
    ::PROTOBUF_NAMESPACE_ID::internal::ArenaStringPtr fingerprint_;
    ::xla::CompileOptionsProto* compile_options_;
    int32_t num_replicas_;
    int32_t num_partitions_;
    mutable ::PROTOBUF_NAMESPACE_ID::internal::CachedSize _cached_size_;
  };
  union { Impl_ _impl_; };
  friend struct ::TableStruct_xla_2fpjrt_2fstream_5fexecutor_5fexecutable_2eproto;
};
// ===================================================================


// ===================================================================

#ifdef __GNUC__
  #pragma GCC diagnostic push
  #pragma GCC diagnostic ignored "-Wstrict-aliasing"
#endif  // __GNUC__
// StreamExecutorExecutableProto

// .xla.CompileOptionsProto compile_options = 1;
inline bool StreamExecutorExecutableProto::_internal_has_compile_options() const {
  return this != internal_default_instance() && _impl_.compile_options_ != nullptr;
}
inline bool StreamExecutorExecutableProto::has_compile_options() const {
  return _internal_has_compile_options();
}
inline const ::xla::CompileOptionsProto& StreamExecutorExecutableProto::_internal_compile_options() const {
  const ::xla::CompileOptionsProto* p = _impl_.compile_options_;
  return p != nullptr ? *p : reinterpret_cast<const ::xla::CompileOptionsProto&>(
      ::xla::_CompileOptionsProto_default_instance_);
}
inline const ::xla::CompileOptionsProto& StreamExecutorExecutableProto::compile_options() const {
  // @@protoc_insertion_point(field_get:xla.StreamExecutorExecutableProto.compile_options)
  return _internal_compile_options();
}
inline void StreamExecutorExecutableProto::unsafe_arena_set_allocated_compile_options(
    ::xla::CompileOptionsProto* compile_options) {
  if (GetArenaForAllocation() == nullptr) {
    delete reinterpret_cast<::PROTOBUF_NAMESPACE_ID::MessageLite*>(_impl_.compile_options_);
  }
  _impl_.compile_options_ = compile_options;
  if (compile_options) {
    
  } else {
    
  }
  // @@protoc_insertion_point(field_unsafe_arena_set_allocated:xla.StreamExecutorExecutableProto.compile_options)
}
inline ::xla::CompileOptionsProto* StreamExecutorExecutableProto::release_compile_options() {
  
  ::xla::CompileOptionsProto* temp = _impl_.compile_options_;
  _impl_.compile_options_ = nullptr;
#ifdef PROTOBUF_FORCE_COPY_IN_RELEASE
  auto* old =  reinterpret_cast<::PROTOBUF_NAMESPACE_ID::MessageLite*>(temp);
  temp = ::PROTOBUF_NAMESPACE_ID::internal::DuplicateIfNonNull(temp);
  if (GetArenaForAllocation() == nullptr) { delete old; }
#else  // PROTOBUF_FORCE_COPY_IN_RELEASE
  if (GetArenaForAllocation() != nullptr) {
    temp = ::PROTOBUF_NAMESPACE_ID::internal::DuplicateIfNonNull(temp);
  }
#endif  // !PROTOBUF_FORCE_COPY_IN_RELEASE
  return temp;
}
inline ::xla::CompileOptionsProto* StreamExecutorExecutableProto::unsafe_arena_release_compile_options() {
  // @@protoc_insertion_point(field_release:xla.StreamExecutorExecutableProto.compile_options)
  
  ::xla::CompileOptionsProto* temp = _impl_.compile_options_;
  _impl_.compile_options_ = nullptr;
  return temp;
}
inline ::xla::CompileOptionsProto* StreamExecutorExecutableProto::_internal_mutable_compile_options() {
  
  if (_impl_.compile_options_ == nullptr) {
    auto* p = CreateMaybeMessage<::xla::CompileOptionsProto>(GetArenaForAllocation());
    _impl_.compile_options_ = p;
  }
  return _impl_.compile_options_;
}
inline ::xla::CompileOptionsProto* StreamExecutorExecutableProto::mutable_compile_options() {
  ::xla::CompileOptionsProto* _msg = _internal_mutable_compile_options();
  // @@protoc_insertion_point(field_mutable:xla.StreamExecutorExecutableProto.compile_options)
  return _msg;
}
inline void StreamExecutorExecutableProto::set_allocated_compile_options(::xla::CompileOptionsProto* compile_options) {
  ::PROTOBUF_NAMESPACE_ID::Arena* message_arena = GetArenaForAllocation();
  if (message_arena == nullptr) {
    delete reinterpret_cast< ::PROTOBUF_NAMESPACE_ID::MessageLite*>(_impl_.compile_options_);
  }
  if (compile_options) {
    ::PROTOBUF_NAMESPACE_ID::Arena* submessage_arena =
        ::PROTOBUF_NAMESPACE_ID::Arena::InternalGetOwningArena(
                reinterpret_cast<::PROTOBUF_NAMESPACE_ID::MessageLite*>(compile_options));
    if (message_arena != submessage_arena) {
      compile_options = ::PROTOBUF_NAMESPACE_ID::internal::GetOwnedMessage(
          message_arena, compile_options, submessage_arena);
    }
    
  } else {
    
  }
  _impl_.compile_options_ = compile_options;
  // @@protoc_insertion_point(field_set_allocated:xla.StreamExecutorExecutableProto.compile_options)
}

// repeated bytes executables = 2;
inline int StreamExecutorExecutableProto::_internal_executables_size() const {
  return _impl_.executables_.size();
}
inline int StreamExecutorExecutableProto::executables_size() const {
  return _internal_executables_size();
}
inline void StreamExecutorExecutableProto::clear_executables() {
  _impl_.executables_.Clear();
}
inline std::string* StreamExecutorExecutableProto::add_executables() {
  std::string* _s = _internal_add_executables();
  // @@protoc_insertion_point(field_add_mutable:xla.StreamExecutorExecutableProto.executables)
  return _s;
}
inline const std::string& StreamExecutorExecutableProto::_internal_executables(int index) const {
  return _impl_.executables_.Get(index);
}
inline const std::string& StreamExecutorExecutableProto::executables(int index) const {
  // @@protoc_insertion_point(field_get:xla.StreamExecutorExecutableProto.executables)
  return _internal_executables(index);
}
inline std::string* StreamExecutorExecutableProto::mutable_executables(int index) {
  // @@protoc_insertion_point(field_mutable:xla.StreamExecutorExecutableProto.executables)
  return _impl_.executables_.Mutable(index);
}
inline void StreamExecutorExecutableProto::set_executables(int index, const std::string& value) {
  _impl_.executables_.Mutable(index)->assign(value);
  // @@protoc_insertion_point(field_set:xla.StreamExecutorExecutableProto.executables)
}
inline void StreamExecutorExecutableProto::set_executables(int index, std::string&& value) {
  _impl_.executables_.Mutable(index)->assign(std::move(value));
  // @@protoc_insertion_point(field_set:xla.StreamExecutorExecutableProto.executables)
}
inline void StreamExecutorExecutableProto::set_executables(int index, const char* value) {
  GOOGLE_DCHECK(value != nullptr);
  _impl_.executables_.Mutable(index)->assign(value);
  // @@protoc_insertion_point(field_set_char:xla.StreamExecutorExecutableProto.executables)
}
inline void StreamExecutorExecutableProto::set_executables(int index, const void* value, size_t size) {
  _impl_.executables_.Mutable(index)->assign(
    reinterpret_cast<const char*>(value), size);
  // @@protoc_insertion_point(field_set_pointer:xla.StreamExecutorExecutableProto.executables)
}
inline std::string* StreamExecutorExecutableProto::_internal_add_executables() {
  return _impl_.executables_.Add();
}
inline void StreamExecutorExecutableProto::add_executables(const std::string& value) {
  _impl_.executables_.Add()->assign(value);
  // @@protoc_insertion_point(field_add:xla.StreamExecutorExecutableProto.executables)
}
inline void StreamExecutorExecutableProto::add_executables(std::string&& value) {
  _impl_.executables_.Add(std::move(value));
  // @@protoc_insertion_point(field_add:xla.StreamExecutorExecutableProto.executables)
}
inline void StreamExecutorExecutableProto::add_executables(const char* value) {
  GOOGLE_DCHECK(value != nullptr);
  _impl_.executables_.Add()->assign(value);
  // @@protoc_insertion_point(field_add_char:xla.StreamExecutorExecutableProto.executables)
}
inline void StreamExecutorExecutableProto::add_executables(const void* value, size_t size) {
  _impl_.executables_.Add()->assign(reinterpret_cast<const char*>(value), size);
  // @@protoc_insertion_point(field_add_pointer:xla.StreamExecutorExecutableProto.executables)
}
inline const ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField<std::string>&
StreamExecutorExecutableProto::executables() const {
  // @@protoc_insertion_point(field_list:xla.StreamExecutorExecutableProto.executables)
  return _impl_.executables_;
}
inline ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField<std::string>*
StreamExecutorExecutableProto::mutable_executables() {
  // @@protoc_insertion_point(field_mutable_list:xla.StreamExecutorExecutableProto.executables)
  return &_impl_.executables_;
}

// int32 num_replicas = 3;
inline void StreamExecutorExecutableProto::clear_num_replicas() {
  _impl_.num_replicas_ = 0;
}
inline int32_t StreamExecutorExecutableProto::_internal_num_replicas() const {
  return _impl_.num_replicas_;
}
inline int32_t StreamExecutorExecutableProto::num_replicas() const {
  // @@protoc_insertion_point(field_get:xla.StreamExecutorExecutableProto.num_replicas)
  return _internal_num_replicas();
}
inline void StreamExecutorExecutableProto::_internal_set_num_replicas(int32_t value) {
  
  _impl_.num_replicas_ = value;
}
inline void StreamExecutorExecutableProto::set_num_replicas(int32_t value) {
  _internal_set_num_replicas(value);
  // @@protoc_insertion_point(field_set:xla.StreamExecutorExecutableProto.num_replicas)
}

// int32 num_partitions = 4;
inline void StreamExecutorExecutableProto::clear_num_partitions() {
  _impl_.num_partitions_ = 0;
}
inline int32_t StreamExecutorExecutableProto::_internal_num_partitions() const {
  return _impl_.num_partitions_;
}
inline int32_t StreamExecutorExecutableProto::num_partitions() const {
  // @@protoc_insertion_point(field_get:xla.StreamExecutorExecutableProto.num_partitions)
  return _internal_num_partitions();
}
inline void StreamExecutorExecutableProto::_internal_set_num_partitions(int32_t value) {
  
  _impl_.num_partitions_ = value;
}
inline void StreamExecutorExecutableProto::set_num_partitions(int32_t value) {
  _internal_set_num_partitions(value);
  // @@protoc_insertion_point(field_set:xla.StreamExecutorExecutableProto.num_partitions)
}

// string name = 5;
inline void StreamExecutorExecutableProto::clear_name() {
  _impl_.name_.ClearToEmpty();
}
inline const std::string& StreamExecutorExecutableProto::name() const {
  // @@protoc_insertion_point(field_get:xla.StreamExecutorExecutableProto.name)
  return _internal_name();
}
template <typename ArgT0, typename... ArgT>
inline PROTOBUF_ALWAYS_INLINE
void StreamExecutorExecutableProto::set_name(ArgT0&& arg0, ArgT... args) {
 
 _impl_.name_.Set(static_cast<ArgT0 &&>(arg0), args..., GetArenaForAllocation());
  // @@protoc_insertion_point(field_set:xla.StreamExecutorExecutableProto.name)
}
inline std::string* StreamExecutorExecutableProto::mutable_name() {
  std::string* _s = _internal_mutable_name();
  // @@protoc_insertion_point(field_mutable:xla.StreamExecutorExecutableProto.name)
  return _s;
}
inline const std::string& StreamExecutorExecutableProto::_internal_name() const {
  return _impl_.name_.Get();
}
inline void StreamExecutorExecutableProto::_internal_set_name(const std::string& value) {
  
  _impl_.name_.Set(value, GetArenaForAllocation());
}
inline std::string* StreamExecutorExecutableProto::_internal_mutable_name() {
  
  return _impl_.name_.Mutable(GetArenaForAllocation());
}
inline std::string* StreamExecutorExecutableProto::release_name() {
  // @@protoc_insertion_point(field_release:xla.StreamExecutorExecutableProto.name)
  return _impl_.name_.Release();
}
inline void StreamExecutorExecutableProto::set_allocated_name(std::string* name) {
  if (name != nullptr) {
    
  } else {
    
  }
  _impl_.name_.SetAllocated(name, GetArenaForAllocation());
#ifdef PROTOBUF_FORCE_COPY_DEFAULT_STRING
  if (_impl_.name_.IsDefault()) {
    _impl_.name_.Set("", GetArenaForAllocation());
  }
#endif // PROTOBUF_FORCE_COPY_DEFAULT_STRING
  // @@protoc_insertion_point(field_set_allocated:xla.StreamExecutorExecutableProto.name)
}

// string fingerprint = 6;
inline void StreamExecutorExecutableProto::clear_fingerprint() {
  _impl_.fingerprint_.ClearToEmpty();
}
inline const std::string& StreamExecutorExecutableProto::fingerprint() const {
  // @@protoc_insertion_point(field_get:xla.StreamExecutorExecutableProto.fingerprint)
  return _internal_fingerprint();
}
template <typename ArgT0, typename... ArgT>
inline PROTOBUF_ALWAYS_INLINE
void StreamExecutorExecutableProto::set_fingerprint(ArgT0&& arg0, ArgT... args) {
 
 _impl_.fingerprint_.Set(static_cast<ArgT0 &&>(arg0), args..., GetArenaForAllocation());
  // @@protoc_insertion_point(field_set:xla.StreamExecutorExecutableProto.fingerprint)
}
inline std::string* StreamExecutorExecutableProto::mutable_fingerprint() {
  std::string* _s = _internal_mutable_fingerprint();
  // @@protoc_insertion_point(field_mutable:xla.StreamExecutorExecutableProto.fingerprint)
  return _s;
}
inline const std::string& StreamExecutorExecutableProto::_internal_fingerprint() const {
  return _impl_.fingerprint_.Get();
}
inline void StreamExecutorExecutableProto::_internal_set_fingerprint(const std::string& value) {
  
  _impl_.fingerprint_.Set(value, GetArenaForAllocation());
}
inline std::string* StreamExecutorExecutableProto::_internal_mutable_fingerprint() {
  
  return _impl_.fingerprint_.Mutable(GetArenaForAllocation());
}
inline std::string* StreamExecutorExecutableProto::release_fingerprint() {
  // @@protoc_insertion_point(field_release:xla.StreamExecutorExecutableProto.fingerprint)
  return _impl_.fingerprint_.Release();
}
inline void StreamExecutorExecutableProto::set_allocated_fingerprint(std::string* fingerprint) {
  if (fingerprint != nullptr) {
    
  } else {
    
  }
  _impl_.fingerprint_.SetAllocated(fingerprint, GetArenaForAllocation());
#ifdef PROTOBUF_FORCE_COPY_DEFAULT_STRING
  if (_impl_.fingerprint_.IsDefault()) {
    _impl_.fingerprint_.Set("", GetArenaForAllocation());
  }
#endif // PROTOBUF_FORCE_COPY_DEFAULT_STRING
  // @@protoc_insertion_point(field_set_allocated:xla.StreamExecutorExecutableProto.fingerprint)
}

#ifdef __GNUC__
  #pragma GCC diagnostic pop
#endif  // __GNUC__

// @@protoc_insertion_point(namespace_scope)

}  // namespace xla

// @@protoc_insertion_point(global_scope)

#include <google/protobuf/port_undef.inc>
#endif  // GOOGLE_PROTOBUF_INCLUDED_GOOGLE_PROTOBUF_INCLUDED_xla_2fpjrt_2fstream_5fexecutor_5fexecutable_2eproto
