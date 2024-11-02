// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: tensorflow/core/framework/tensor_shape.proto

#ifndef GOOGLE_PROTOBUF_INCLUDED_tensorflow_2fcore_2fframework_2ftensor_5fshape_2eproto
#define GOOGLE_PROTOBUF_INCLUDED_tensorflow_2fcore_2fframework_2ftensor_5fshape_2eproto

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
#define PROTOBUF_INTERNAL_EXPORT_tensorflow_2fcore_2fframework_2ftensor_5fshape_2eproto PROTOBUF_EXPORT
PROTOBUF_NAMESPACE_OPEN
namespace internal {
class AnyMetadata;
}  // namespace internal
PROTOBUF_NAMESPACE_CLOSE

// Internal implementation detail -- do not use these members.
struct PROTOBUF_EXPORT TableStruct_tensorflow_2fcore_2fframework_2ftensor_5fshape_2eproto {
  static const uint32_t offsets[];
};
PROTOBUF_EXPORT extern const ::PROTOBUF_NAMESPACE_ID::internal::DescriptorTable descriptor_table_tensorflow_2fcore_2fframework_2ftensor_5fshape_2eproto;
namespace tensorflow {
class TensorShapeProto;
struct TensorShapeProtoDefaultTypeInternal;
PROTOBUF_EXPORT extern TensorShapeProtoDefaultTypeInternal _TensorShapeProto_default_instance_;
class TensorShapeProto_Dim;
struct TensorShapeProto_DimDefaultTypeInternal;
PROTOBUF_EXPORT extern TensorShapeProto_DimDefaultTypeInternal _TensorShapeProto_Dim_default_instance_;
}  // namespace tensorflow
PROTOBUF_NAMESPACE_OPEN
template<> PROTOBUF_EXPORT ::tensorflow::TensorShapeProto* Arena::CreateMaybeMessage<::tensorflow::TensorShapeProto>(Arena*);
template<> PROTOBUF_EXPORT ::tensorflow::TensorShapeProto_Dim* Arena::CreateMaybeMessage<::tensorflow::TensorShapeProto_Dim>(Arena*);
PROTOBUF_NAMESPACE_CLOSE
namespace tensorflow {

// ===================================================================

class PROTOBUF_EXPORT TensorShapeProto_Dim final :
    public ::PROTOBUF_NAMESPACE_ID::Message /* @@protoc_insertion_point(class_definition:tensorflow.TensorShapeProto.Dim) */ {
 public:
  inline TensorShapeProto_Dim() : TensorShapeProto_Dim(nullptr) {}
  ~TensorShapeProto_Dim() override;
  explicit PROTOBUF_CONSTEXPR TensorShapeProto_Dim(::PROTOBUF_NAMESPACE_ID::internal::ConstantInitialized);

  TensorShapeProto_Dim(const TensorShapeProto_Dim& from);
  TensorShapeProto_Dim(TensorShapeProto_Dim&& from) noexcept
    : TensorShapeProto_Dim() {
    *this = ::std::move(from);
  }

  inline TensorShapeProto_Dim& operator=(const TensorShapeProto_Dim& from) {
    CopyFrom(from);
    return *this;
  }
  inline TensorShapeProto_Dim& operator=(TensorShapeProto_Dim&& from) noexcept {
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
  static const TensorShapeProto_Dim& default_instance() {
    return *internal_default_instance();
  }
  static inline const TensorShapeProto_Dim* internal_default_instance() {
    return reinterpret_cast<const TensorShapeProto_Dim*>(
               &_TensorShapeProto_Dim_default_instance_);
  }
  static constexpr int kIndexInFileMessages =
    0;

  friend void swap(TensorShapeProto_Dim& a, TensorShapeProto_Dim& b) {
    a.Swap(&b);
  }
  inline void Swap(TensorShapeProto_Dim* other) {
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
  void UnsafeArenaSwap(TensorShapeProto_Dim* other) {
    if (other == this) return;
    GOOGLE_DCHECK(GetOwningArena() == other->GetOwningArena());
    InternalSwap(other);
  }

  // implements Message ----------------------------------------------

  TensorShapeProto_Dim* New(::PROTOBUF_NAMESPACE_ID::Arena* arena = nullptr) const final {
    return CreateMaybeMessage<TensorShapeProto_Dim>(arena);
  }
  using ::PROTOBUF_NAMESPACE_ID::Message::CopyFrom;
  void CopyFrom(const TensorShapeProto_Dim& from);
  using ::PROTOBUF_NAMESPACE_ID::Message::MergeFrom;
  void MergeFrom( const TensorShapeProto_Dim& from) {
    TensorShapeProto_Dim::MergeImpl(*this, from);
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
  void InternalSwap(TensorShapeProto_Dim* other);

  private:
  friend class ::PROTOBUF_NAMESPACE_ID::internal::AnyMetadata;
  static ::PROTOBUF_NAMESPACE_ID::StringPiece FullMessageName() {
    return "tensorflow.TensorShapeProto.Dim";
  }
  protected:
  explicit TensorShapeProto_Dim(::PROTOBUF_NAMESPACE_ID::Arena* arena,
                       bool is_message_owned = false);
  public:

  static const ClassData _class_data_;
  const ::PROTOBUF_NAMESPACE_ID::Message::ClassData*GetClassData() const final;

  ::PROTOBUF_NAMESPACE_ID::Metadata GetMetadata() const final;

  // nested types ----------------------------------------------------

  // accessors -------------------------------------------------------

  enum : int {
    kNameFieldNumber = 2,
    kSizeFieldNumber = 1,
  };
  // string name = 2;
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

  // int64 size = 1;
  void clear_size();
  int64_t size() const;
  void set_size(int64_t value);
  private:
  int64_t _internal_size() const;
  void _internal_set_size(int64_t value);
  public:

  // @@protoc_insertion_point(class_scope:tensorflow.TensorShapeProto.Dim)
 private:
  class _Internal;

  template <typename T> friend class ::PROTOBUF_NAMESPACE_ID::Arena::InternalHelper;
  typedef void InternalArenaConstructable_;
  typedef void DestructorSkippable_;
  struct Impl_ {
    ::PROTOBUF_NAMESPACE_ID::internal::ArenaStringPtr name_;
    int64_t size_;
    mutable ::PROTOBUF_NAMESPACE_ID::internal::CachedSize _cached_size_;
  };
  union { Impl_ _impl_; };
  friend struct ::TableStruct_tensorflow_2fcore_2fframework_2ftensor_5fshape_2eproto;
};
// -------------------------------------------------------------------

class PROTOBUF_EXPORT TensorShapeProto final :
    public ::PROTOBUF_NAMESPACE_ID::Message /* @@protoc_insertion_point(class_definition:tensorflow.TensorShapeProto) */ {
 public:
  inline TensorShapeProto() : TensorShapeProto(nullptr) {}
  ~TensorShapeProto() override;
  explicit PROTOBUF_CONSTEXPR TensorShapeProto(::PROTOBUF_NAMESPACE_ID::internal::ConstantInitialized);

  TensorShapeProto(const TensorShapeProto& from);
  TensorShapeProto(TensorShapeProto&& from) noexcept
    : TensorShapeProto() {
    *this = ::std::move(from);
  }

  inline TensorShapeProto& operator=(const TensorShapeProto& from) {
    CopyFrom(from);
    return *this;
  }
  inline TensorShapeProto& operator=(TensorShapeProto&& from) noexcept {
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
  static const TensorShapeProto& default_instance() {
    return *internal_default_instance();
  }
  static inline const TensorShapeProto* internal_default_instance() {
    return reinterpret_cast<const TensorShapeProto*>(
               &_TensorShapeProto_default_instance_);
  }
  static constexpr int kIndexInFileMessages =
    1;

  friend void swap(TensorShapeProto& a, TensorShapeProto& b) {
    a.Swap(&b);
  }
  inline void Swap(TensorShapeProto* other) {
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
  void UnsafeArenaSwap(TensorShapeProto* other) {
    if (other == this) return;
    GOOGLE_DCHECK(GetOwningArena() == other->GetOwningArena());
    InternalSwap(other);
  }

  // implements Message ----------------------------------------------

  TensorShapeProto* New(::PROTOBUF_NAMESPACE_ID::Arena* arena = nullptr) const final {
    return CreateMaybeMessage<TensorShapeProto>(arena);
  }
  using ::PROTOBUF_NAMESPACE_ID::Message::CopyFrom;
  void CopyFrom(const TensorShapeProto& from);
  using ::PROTOBUF_NAMESPACE_ID::Message::MergeFrom;
  void MergeFrom( const TensorShapeProto& from) {
    TensorShapeProto::MergeImpl(*this, from);
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
  void InternalSwap(TensorShapeProto* other);

  private:
  friend class ::PROTOBUF_NAMESPACE_ID::internal::AnyMetadata;
  static ::PROTOBUF_NAMESPACE_ID::StringPiece FullMessageName() {
    return "tensorflow.TensorShapeProto";
  }
  protected:
  explicit TensorShapeProto(::PROTOBUF_NAMESPACE_ID::Arena* arena,
                       bool is_message_owned = false);
  public:

  static const ClassData _class_data_;
  const ::PROTOBUF_NAMESPACE_ID::Message::ClassData*GetClassData() const final;

  ::PROTOBUF_NAMESPACE_ID::Metadata GetMetadata() const final;

  // nested types ----------------------------------------------------

  typedef TensorShapeProto_Dim Dim;

  // accessors -------------------------------------------------------

  enum : int {
    kDimFieldNumber = 2,
    kUnknownRankFieldNumber = 3,
  };
  // repeated .tensorflow.TensorShapeProto.Dim dim = 2;
  int dim_size() const;
  private:
  int _internal_dim_size() const;
  public:
  void clear_dim();
  ::tensorflow::TensorShapeProto_Dim* mutable_dim(int index);
  ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField< ::tensorflow::TensorShapeProto_Dim >*
      mutable_dim();
  private:
  const ::tensorflow::TensorShapeProto_Dim& _internal_dim(int index) const;
  ::tensorflow::TensorShapeProto_Dim* _internal_add_dim();
  public:
  const ::tensorflow::TensorShapeProto_Dim& dim(int index) const;
  ::tensorflow::TensorShapeProto_Dim* add_dim();
  const ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField< ::tensorflow::TensorShapeProto_Dim >&
      dim() const;

  // bool unknown_rank = 3;
  void clear_unknown_rank();
  bool unknown_rank() const;
  void set_unknown_rank(bool value);
  private:
  bool _internal_unknown_rank() const;
  void _internal_set_unknown_rank(bool value);
  public:

  // @@protoc_insertion_point(class_scope:tensorflow.TensorShapeProto)
 private:
  class _Internal;

  template <typename T> friend class ::PROTOBUF_NAMESPACE_ID::Arena::InternalHelper;
  typedef void InternalArenaConstructable_;
  typedef void DestructorSkippable_;
  struct Impl_ {
    ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField< ::tensorflow::TensorShapeProto_Dim > dim_;
    bool unknown_rank_;
    mutable ::PROTOBUF_NAMESPACE_ID::internal::CachedSize _cached_size_;
  };
  union { Impl_ _impl_; };
  friend struct ::TableStruct_tensorflow_2fcore_2fframework_2ftensor_5fshape_2eproto;
};
// ===================================================================


// ===================================================================

#ifdef __GNUC__
  #pragma GCC diagnostic push
  #pragma GCC diagnostic ignored "-Wstrict-aliasing"
#endif  // __GNUC__
// TensorShapeProto_Dim

// int64 size = 1;
inline void TensorShapeProto_Dim::clear_size() {
  _impl_.size_ = int64_t{0};
}
inline int64_t TensorShapeProto_Dim::_internal_size() const {
  return _impl_.size_;
}
inline int64_t TensorShapeProto_Dim::size() const {
  // @@protoc_insertion_point(field_get:tensorflow.TensorShapeProto.Dim.size)
  return _internal_size();
}
inline void TensorShapeProto_Dim::_internal_set_size(int64_t value) {
  
  _impl_.size_ = value;
}
inline void TensorShapeProto_Dim::set_size(int64_t value) {
  _internal_set_size(value);
  // @@protoc_insertion_point(field_set:tensorflow.TensorShapeProto.Dim.size)
}

// string name = 2;
inline void TensorShapeProto_Dim::clear_name() {
  _impl_.name_.ClearToEmpty();
}
inline const std::string& TensorShapeProto_Dim::name() const {
  // @@protoc_insertion_point(field_get:tensorflow.TensorShapeProto.Dim.name)
  return _internal_name();
}
template <typename ArgT0, typename... ArgT>
inline PROTOBUF_ALWAYS_INLINE
void TensorShapeProto_Dim::set_name(ArgT0&& arg0, ArgT... args) {
 
 _impl_.name_.Set(static_cast<ArgT0 &&>(arg0), args..., GetArenaForAllocation());
  // @@protoc_insertion_point(field_set:tensorflow.TensorShapeProto.Dim.name)
}
inline std::string* TensorShapeProto_Dim::mutable_name() {
  std::string* _s = _internal_mutable_name();
  // @@protoc_insertion_point(field_mutable:tensorflow.TensorShapeProto.Dim.name)
  return _s;
}
inline const std::string& TensorShapeProto_Dim::_internal_name() const {
  return _impl_.name_.Get();
}
inline void TensorShapeProto_Dim::_internal_set_name(const std::string& value) {
  
  _impl_.name_.Set(value, GetArenaForAllocation());
}
inline std::string* TensorShapeProto_Dim::_internal_mutable_name() {
  
  return _impl_.name_.Mutable(GetArenaForAllocation());
}
inline std::string* TensorShapeProto_Dim::release_name() {
  // @@protoc_insertion_point(field_release:tensorflow.TensorShapeProto.Dim.name)
  return _impl_.name_.Release();
}
inline void TensorShapeProto_Dim::set_allocated_name(std::string* name) {
  if (name != nullptr) {
    
  } else {
    
  }
  _impl_.name_.SetAllocated(name, GetArenaForAllocation());
#ifdef PROTOBUF_FORCE_COPY_DEFAULT_STRING
  if (_impl_.name_.IsDefault()) {
    _impl_.name_.Set("", GetArenaForAllocation());
  }
#endif // PROTOBUF_FORCE_COPY_DEFAULT_STRING
  // @@protoc_insertion_point(field_set_allocated:tensorflow.TensorShapeProto.Dim.name)
}

// -------------------------------------------------------------------

// TensorShapeProto

// repeated .tensorflow.TensorShapeProto.Dim dim = 2;
inline int TensorShapeProto::_internal_dim_size() const {
  return _impl_.dim_.size();
}
inline int TensorShapeProto::dim_size() const {
  return _internal_dim_size();
}
inline void TensorShapeProto::clear_dim() {
  _impl_.dim_.Clear();
}
inline ::tensorflow::TensorShapeProto_Dim* TensorShapeProto::mutable_dim(int index) {
  // @@protoc_insertion_point(field_mutable:tensorflow.TensorShapeProto.dim)
  return _impl_.dim_.Mutable(index);
}
inline ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField< ::tensorflow::TensorShapeProto_Dim >*
TensorShapeProto::mutable_dim() {
  // @@protoc_insertion_point(field_mutable_list:tensorflow.TensorShapeProto.dim)
  return &_impl_.dim_;
}
inline const ::tensorflow::TensorShapeProto_Dim& TensorShapeProto::_internal_dim(int index) const {
  return _impl_.dim_.Get(index);
}
inline const ::tensorflow::TensorShapeProto_Dim& TensorShapeProto::dim(int index) const {
  // @@protoc_insertion_point(field_get:tensorflow.TensorShapeProto.dim)
  return _internal_dim(index);
}
inline ::tensorflow::TensorShapeProto_Dim* TensorShapeProto::_internal_add_dim() {
  return _impl_.dim_.Add();
}
inline ::tensorflow::TensorShapeProto_Dim* TensorShapeProto::add_dim() {
  ::tensorflow::TensorShapeProto_Dim* _add = _internal_add_dim();
  // @@protoc_insertion_point(field_add:tensorflow.TensorShapeProto.dim)
  return _add;
}
inline const ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField< ::tensorflow::TensorShapeProto_Dim >&
TensorShapeProto::dim() const {
  // @@protoc_insertion_point(field_list:tensorflow.TensorShapeProto.dim)
  return _impl_.dim_;
}

// bool unknown_rank = 3;
inline void TensorShapeProto::clear_unknown_rank() {
  _impl_.unknown_rank_ = false;
}
inline bool TensorShapeProto::_internal_unknown_rank() const {
  return _impl_.unknown_rank_;
}
inline bool TensorShapeProto::unknown_rank() const {
  // @@protoc_insertion_point(field_get:tensorflow.TensorShapeProto.unknown_rank)
  return _internal_unknown_rank();
}
inline void TensorShapeProto::_internal_set_unknown_rank(bool value) {
  
  _impl_.unknown_rank_ = value;
}
inline void TensorShapeProto::set_unknown_rank(bool value) {
  _internal_set_unknown_rank(value);
  // @@protoc_insertion_point(field_set:tensorflow.TensorShapeProto.unknown_rank)
}

#ifdef __GNUC__
  #pragma GCC diagnostic pop
#endif  // __GNUC__
// -------------------------------------------------------------------


// @@protoc_insertion_point(namespace_scope)

}  // namespace tensorflow

// @@protoc_insertion_point(global_scope)

#include <google/protobuf/port_undef.inc>
#endif  // GOOGLE_PROTOBUF_INCLUDED_GOOGLE_PROTOBUF_INCLUDED_tensorflow_2fcore_2fframework_2ftensor_5fshape_2eproto
