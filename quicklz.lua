
local ffi = require "ffi"
if not ffi then
  error("load ffi failed!")
  return
end
--  $ gcc -P -E quicklz.h
-- after deleting some relevent code
ffi.cdef[[
typedef unsigned int ui32;
typedef unsigned short int ui16;
typedef struct
{
 ui32 cache;
 unsigned int offset;
} qlz_hash_compress;
typedef struct
{
 const unsigned char *offset;
} qlz_hash_decompress;
typedef struct
{
 size_t stream_counter;
 qlz_hash_compress hash[4096];
 unsigned char hash_counter[4096];
} qlz_state_compress;


 typedef struct
 {



  qlz_hash_decompress hash[4096];
  unsigned char hash_counter[4096];
  size_t stream_counter;
 } qlz_state_decompress;
size_t qlz_size_decompressed(const char *source);
size_t qlz_size_compressed(const char *source);
size_t qlz_compress(const void *source, char *destination, size_t size, qlz_state_compress *state);
size_t qlz_decompress(const char *source, void *destination, qlz_state_decompress *state);
int qlz_get_setting(int setting);
]]

local quicklz = ffi.load("/opt/source/local/quicklz15.so",true)
if not quicklz then
  error("load quicklz failed!")
  return
end

function compress(txt)
	n          = #txt
	st         = ffi.new("qlz_state_compress[1]")
	compressed = ffi.new("uint8_t[?]", n+400)
	quicklz.qlz_compress(txt, compressed, n, st)
    sz = quicklz.qlz_size_compressed(compressed)
	return ffi.string(compressed, sz)
end

function decompress(txt)
	st = ffi.new("qlz_state_decompress[1]")
	sz = quicklz.qlz_size_decompressed(txt)
	decompressed = ffi.new("uint8_t[?]", sz+1)
	quicklz.qlz_decompress(txt, decompressed, st)
	return ffi.string(decompressed, sz)
end

ngx.req.read_body()
local method = ngx.var.request_method
ngx.say("request_method:\t",method)

if method ~= 'POST' then
    ngx.say('pls. /=/quicklz only work as POST ;-)')
else
    local txt=""
    local res = ngx.location.capture("/memc",{args={key = "p_promo_8260"}})
    if res.status == 200 then  
         txt=res.body     
    end  
    print("Uncompressed size: ", #txt)
    local c = compress(txt)
    print("Compressed size: ", #c)
    local txt2 = decompress(c)
    assert(txt2 == txt)
    ngx.say(c)
    ngx.say(txt2)
end
