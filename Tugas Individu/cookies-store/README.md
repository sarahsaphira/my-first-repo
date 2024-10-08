# TUGAS INDIVIDU 6
1. Jelaskan manfaat dari penggunaan JavaScript dalam pengembangan aplikasi web!

JavaScript memiliki banyak manfaat dalam pengembangan aplikasi web. Salah satu keunggulannya adalah kemampuannya untuk menciptakan halaman web yang interaktif dan dinamis. Selain itu karena berjalan di sisi klien (browser), JavaScript dapat mengurangi beban server dan meningkatkan kecepatan eksekusi tugas-tugas sederhana, seperti memanipulasi elemen HTML dan CSS secara real-time. Penggunaan JavaScript juga memungkinkan pengembangan aplikasi berbasis Single Page Application (SPA), di mana konten halaman diperbarui secara dinamis tanpa memuat ulang seluruh halaman, sehingga memberikan pengalaman yang lebih responsif bagi pengguna. 

Dengan dukungan dari berbagai perangkat dan platform, JavaScript memudahkan pengembangan aplikasi web lintas platform. Selain itu, kemampuan JavaScript dalam menangani pemrosesan asynchronous melalui AJAX atau fetch() juga memungkinkan komunikasi data dengan server tanpa mengganggu pengalaman pengguna. Dengan dukungan komunitas yang besar dan beragam pustaka open-source, JavaScript telah menjadi bahasa yang sangat penting dalam pengembangan aplikasi web modern.

2. Jelaskan fungsi dari penggunaan await ketika kita menggunakan fetch()! Apa yang akan terjadi jika kita tidak menggunakan await?

Fungsi dari penggunaan await ketika kita menggunakan fetch() adalah untuk menunggu hasil dari operasi fetch() secara asinkron sebelum melanjutkan eksekusi kode berikutnya. fetch() sendiri mengembalikan sebuah Promise, yang merupakan objek yang mewakili operasi asinkron. Dengan menggunakan await, kita memberitahu JavaScript untuk menghentikan eksekusi sementara dan menunggu hingga operasi fetch() selesai dan nilai yang dijanjikan (resolved) oleh Promise tersebut tersedia.

Jika kita tidak menggunakan await, fetch() akan segera mengembalikan Promise yang belum diselesaikan, dan eksekusi kode akan langsung melanjutkan tanpa menunggu hasil dari fetch(). Ini berarti variabel yang seharusnya menyimpan hasil dari Promise akan berisi objek Promise itu sendiri, bukan data yang diinginkan.
Dengan kata lain, jika tidak menggunakan await, kita harus menggunakan pendekatan berbasis callback dengan .then() untuk menangani hasil Promise, yang bisa membuat kode lebih sulit dibaca dibandingkan dengan pendekatan menggunakan await

3. Mengapa kita perlu menggunakan decorator csrf_exempt pada view yang akan digunakan untuk AJAX POST?

Penggunaan @csrf_exempt pada view yang digunakan untuk menerima AJAX POST diperlukan dalam beberapa situasi karena mekanisme CSRF yang diterapkan oleh Django untuk melindungi aplikasi dari serangan CSRF. Secara default, Django mengharuskan setiap POST request yang diterima dari pengguna untuk menyertakan CSRF token yang valid, yang biasanya dihasilkan dan disematkan pada halaman HTML yang dikirimkan kepada klien.

Namun, dalam konteks AJAX requests, terutama jika permintaan dibuat tanpa menggunakan mekanisme bawaan Django untuk memasukkan CSRF token, server akan menolak permintaan tersebut karena tidak ada token CSRF yang valid. Untuk menghindari penolakan tersebut, kita bisa menggunakan @csrf_exempt untuk mengecualikan view tertentu dari pemeriksaan CSRF.

Akan tetapi, perlu dicatat bahwa menggunakan @csrf_exempt menghilangkan perlindungan CSRF pada view tersebut, sehingga view menjadi lebih rentan terhadap serangan CSRF jika tidak ditangani dengan hati-hati. Karena itu, @csrf_exempt biasanya hanya digunakan jika kita yakin bahwa keamanan tetap terjaga, misalnya saat permintaan hanya berasal dari sumber terpercaya atau ketika mekanisme keamanan lainnya diterapkan, seperti validasi origin atau otentikasi tambahan.
 
4. Pada tutorial PBP minggu ini, pembersihan data input pengguna dilakukan di belakang (backend) juga. Mengapa hal tersebut tidak dilakukan di frontend saja?

Pada tutorial Pemrograman Berbasis Platform (PBP) minggu ini, proses pembersihan atau validasi data input pengguna dilakukan di sisi backend, dan bukan hanya di frontend. Meskipun validasi di frontend penting untuk memberikan umpan balik langsung kepada pengguna, sangat penting juga untuk melakukannya di backend untuk alasan keamanan. Hal ini disebabkan oleh kenyataan bahwa seorang hacker atau pihak yang tidak bertanggung jawab bisa saja melewati validasi frontend dengan mengirimkan request langsung ke server melalui API, tanpa menggunakan antarmuka aplikasi web (frontend) yang telah disediakan. Jika validasi hanya dilakukan di frontend, maka server rentan terhadap serangan seperti injeksi SQL, skrip lintas situs (XSS), atau pengiriman data yang tidak valid atau berbahaya. Oleh karena itu, pembersihan data input di backend diperlukan untuk memastikan bahwa hanya data yang valid dan aman yang diproses oleh sistem, sehingga risiko serangan dapat diminimalkan dan keamanan aplikasi dapat dijaga.

5. Jelaskan bagaimana cara kamu mengimplementasikan checklist di atas secara step-by-step (bukan hanya sekadar mengikuti tutorial)!

- Menambahkan kondisi else pada login_user untuk memastikan pengguna mendapat feedback jika terjadi kesalahan login
```html
else:
    messages.error(request, "Invalid username or password. Please try again.")
```

- Membuat fungsi add_product_ajax pada views. Tambahkan fungsi ini untuk menangani permintaan AJAX untuk menambah produk baru. Fungsi ini menangkap data produk yang dikirim melalui POST, lalu menyimpan data tersebut ke database.
```html
@csrf_exempt
@require_POST
def add_product_ajax(request):
    name = strip_tags(request.POST.get("name"))
    description = strip_tags(request.POST.get("description"))
    price = request.POST.get("price")
    user = request.user

    new_product = Product(
        name=name, description=description,
        price=price,
        user=user
    )
    new_product.save()

    return HttpResponse(b"CREATED", status=201)
```

- Menambahkan routing untuk add_product_ajax. Di dalam urls.py, tambahkan route untuk endpoint create-product-ajax yang akan memanggil fungsi AJAX di views.
```html
path('create-product-ajax', add_product_ajax, name='add_product_ajax'),
```

- Pada fungsi show_json dan show_xml, ubah filter untuk hanya menampilkan produk yang dibuat oleh pengguna yang sedang login.
```html
data = Product.objects.filter(user=request.user)
```

- Hapus blok yang memeriksa kondisi produk dan ganti dengan div kosong untuk meletakkan data produk yang akan ditampilkan dengan JavaScript.
```html
<div id="product_cards"></div>
```

- Menambahkan <script> di bagian bawah template sebelum {% endblock content %}. Fungsi getProducts ini akan mengambil data produk dari endpoint JSON dan menampilkannya pada halaman.
```html
<script>
  async function getProducts() {
      return fetch("{% url 'add_product_ajax' %}").then((res) => res.json());
  }
</script>
```

- Menambahkan fungsi lain yang bertanggung jawab untuk me-refresh tampilan produk setelah data baru ditambahkan atau halaman di-load.
```html
async function refreshProducts() {
    document.getElementById("product_cards").innerHTML = "";
    document.getElementById("product_cards").className = "";
    const products = await getProducts();
    ...
}
```

- Setelah div dengan ID product_cards, tambahkan modal dengan menggunakan Tailwind CSS yang akan memungkinkan pengguna untuk menambah produk baru melalui AJAX. Modal ini berisi form sederhana untuk input data produk.
```html
<div id="crudModal" tabindex="-1" aria-hidden="true" class="hidden fixed inset-0 z-50 ...">
  <!-- Konten modal -->
</div>

```

- Tambahkan event listener pada form modal untuk mengirimkan data produk baru melalui AJAX tanpa reload halaman.
```html
document.getElementById("productForm").addEventListener("submit", (e) => {
    e.preventDefault();
    hideModal();
    addProduct();
  })
```

- Akhirnya, setelah semua bagian diimplementasikan, pastikan untuk melakukan pengujian menyeluruh untuk memastikan bahwa semua fitur berfungsi seperti yang diharapkan.

# TUGAS INDIVIDU 5
1. Jika terdapat beberapa CSS selector untuk suatu elemen HTML, jelaskan urutan prioritas pengambilan CSS selector tersebut!

Dalam CSS, ketika ada beberapa selector yang dapat diterapkan pada elemen HTML yang sama, urutan prioritas pengambilan (juga dikenal sebagai spesifisitas) digunakan untuk menentukan mana yang akan diterapkan. Berikut adalah urutan prioritas spesifisitas CSS:

- Inline Styles
Style yang ditetapkan langsung pada elemen menggunakan atribut style.
Contoh: <div style="color: red;">Contoh</div>

- ID Selector
Selector yang menggunakan ID, yang ditandai dengan simbol #.
Contoh: #header { color: blue; }
Spesifisitasnya adalah 1-0-0.

- Class, Attribute, dan Pseudo-classes Selector
Selector yang menggunakan kelas (.), atribut ([]), atau pseudo-classes (:hover, :first-child, dll.).
Contoh: .menu { color: green; }, [type="text"] { background: yellow; }
Spesifisitasnya adalah 0-1-0.

- Element dan Pseudo-elements Selector
Selector yang menggunakan elemen HTML atau pseudo-elements (::before, ::after, dll.).
Contoh: div { font-size: 16px; }
Spesifisitasnya adalah 0-0-1.

Menghitung Spesifisitas
Setiap selector dapat dihitung spesifisitasnya dalam format (a-b-c):
a: jumlah inline styles.
b: jumlah ID selectors.
c: jumlah class, attribute, dan pseudo-class selectors.
d: jumlah element dan pseudo-element selectors.

Jika spesifisitas sama, aturan yang ditulis terakhir dalam stylesheet akan diterapkan.
Penggunaan !important dapat mengubah urutan prioritas, sehingga CSS dengan !important akan diterapkan terlepas dari spesifisitas lainnya, meskipun sebaiknya digunakan dengan hati-hati karena dapat membuat debugging lebih sulit.

2. Mengapa responsive design menjadi konsep yang penting dalam pengembangan aplikasi web? Berikan contoh aplikasi yang sudah dan belum menerapkan responsive design!

Responsive design sangat penting dalam pengembangan aplikasi web karena memungkinkan tampilan situs beradaptasi secara otomatis dengan berbagai perangkat seperti smartphone, tablet, dan desktop. Dengan adanya responsive design, pengguna dapat menikmati pengalaman yang konsisten dan nyaman tanpa perlu khawatir tentang ukuran layar atau orientasi perangkat. Seiring dengan meningkatnya jumlah pengguna internet yang mengakses melalui perangkat mobile, penerapan responsive design menjadi kunci agar aplikasi tetap mudah diakses dan digunakan di berbagai platform.

Selain itu, responsive design juga mengoptimalkan proses pengembangan dan pemeliharaan situs. Dengan hanya perlu membuat satu versi situs yang dapat berfungsi di berbagai perangkat, pengembang dapat menghemat waktu dan biaya dibandingkan harus membuat versi terpisah untuk desktop dan mobile.

Contoh aplikasi yang telah berhasil menerapkan responsive design adalah Twitter dan Spotify, di mana tata letak dan fitur mereka otomatis menyesuaikan dengan baik di berbagai perangkat. Sebaliknya, beberapa situs berita lama yang belum mengadopsi responsive design masih memerlukan zoom dan scrolling horizontal pada perangkat mobile seperti web berita, yang secara signifikan mengurangi kenyamanan pengalaman pengguna.

3. Jelaskan perbedaan antara margin, border, dan padding, serta cara untuk mengimplementasikan ketiga hal tersebut!

Margin
- Merupakan space antara suatu elemen (bagian luarnya) dengan elemen-elemen lain (di luar elemen itu sendiri)
- Digunakan untuk mengatur spacing di luar elemen (dari sisi luar elemen itu sendiri)
- Berpengaruh terhadap elemen-elemen lain di sekitar elemen yang bersangkutan
- Penerapan: Di CSS, margin dapat diatur menggunakan properti margin, contoh: margin: 10px; untuk memberikan margin 10px di semua sisi elemen.

Border
- Merupakan garis yang mengelilingi elemen, terletak di antara margin dan padding. Border membentuk tepi visual dari elemen.
- Digunakan untuk memberikan batas visual pada elemen, menonjolkan atau membatasi area elemen tersebut.
- Tidak mempengaruhi jarak antara elemen, tetapi dapat menambah ukuran elemen karena border ditambahkan di luar padding.
- Penerapan: Di CSS, border dapat diatur menggunakan properti border, contoh: border: 2px solid black; untuk memberikan border hitam solid dengan ketebalan 2px di sekeliling elemen.

Padding
- Merupakan space antara batas suatu elemen dengan konten yang ada di dalam elemen itu sendiri
- Digunakan untuk mengatur spacing di dalam elemen (dari sisi dalam elemen itu sendiri)
- Hanya memengaruhi elemen itu sendiri
- Penerapan: Di CSS, padding dapat diatur menggunakan properti padding, contoh: padding: 15px; untuk memberikan padding 15px di dalam elemen dari semua sisi.

4. Jelaskan konsep flex box dan grid layout beserta kegunaannya!

- Flexbox (Flexible Box Layout)
Konsep
Flexbox adalah metode tata letak yang dirancang untuk mengatur elemen dalam satu arah, baik secara horizontal maupun vertikal, sehingga memudahkan pembuatan tata letak yang fleksibel dan dinamis. Flexbox mengatur elemen sebagai "flex container" dan "flex items". Dalam Flexbox, elemen-elemen diatur sepanjang satu sumbu utama dan bisa meluas untuk mengisi ruang yang tersedia atau menyusut agar tetap sesuai di dalam kontainer.

Kegunaan:
- Digunakan untuk tata letak yang lebih fleksibel, terutama untuk baris atau kolom tunggal.
- Membuat elemen-elemen dalam container dapat dengan mudah diatur dalam hal ukuran, perataan (alignment), dan distribusi ruang antar-elemen.
- Berguna ketika tata letak harus dapat menyesuaikan dengan ukuran layar yang berbeda (responsive design).

- Grid Layout
Konsep:
Grid Layout adalah metode tata letak yang lebih canggih dibanding Flexbox, di mana elemen-elemen diatur dalam bentuk grid dua dimensi (baris dan kolom). Grid layout memungkinkan pengaturan elemen secara lebih kompleks dalam dua arah (baik horizontal maupun vertikal).
Grid layout mengandalkan penggunaan grid lines untuk menentukan di mana elemen-elemen harus ditempatkan.

Kegunaan:
- Digunakan untuk tata letak yang lebih rumit yang membutuhkan pengaturan elemen-elemen dalam dua arah (baris dan kolom) sekaligus.
- Berguna untuk membuat tata letak halaman yang lebih kompleks dan teratur, seperti layout halaman web yang memiliki header, sidebar, konten utama, dan footer.

5. Jelaskan bagaimana cara kamu mengimplementasikan checklist di atas secara step-by-step (bukan hanya sekadar mengikuti tutorial)!

- Kustomisasi halaman login, register, dan tambah inventori semenarik mungkin.

Halaman Login (login.html):
- Penempatan form dalam card: Saya meletakkan form login dalam sebuah card dengan menggunakan Flexbox dari Tailwind CSS untuk menempatkan card di tengah halaman. Ini memastikan bahwa elemen login terlihat proporsional di berbagai ukuran layar.
- Styling form: Menggunakan Tailwind CSS, saya mengubah tampilan form input untuk username dan password agar lebih modern dengan class form-control. Ini termasuk border, focus state, dan spacing yang lebih elegan.
- Pesan error atau sukses: Implementasi feedback dengan {% if messages %} memungkinkan pesan muncul secara dinamis saat ada kesalahan atau keberhasilan login. Saya menggunakan berbagai warna untuk menunjukkan pesan sesuai kategori (error, success, atau lainnya).
- Tata letak: Layout login diletakkan dalam div dengan properti CSS min-h-screen dan justify-center untuk memastikan card selalu berada di tengah halaman, bahkan saat layar lebih kecil.

Halaman Tambah Produk (create_product.html):
- Card untuk form: Seperti pada halaman login, form untuk menambah produk juga diletakkan dalam card menggunakan container Flexbox yang memusatkan form pada layar. Ini menjaga konsistensi layout di seluruh aplikasi.
- Form handling: Saya menggunakan Django form framework untuk menangani form fields secara otomatis. Setiap field dikustomisasi dengan label dan pesan error yang muncul jika input tidak valid.
- Styling button: Tombol submit diberi gaya menggunakan Tailwind CSS dengan warna cokelat khas (#8B4513) dan efek hover yang lebih menarik, menambah interaktivitas halaman.

Halaman Daftar Inventori (main.html):
- Navbar: Saya membuat sebuah navbar yang terletak di bagian atas halaman dengan opsi navigasi seperti home, produk, kategori, dan cart. Pengguna yang login ditampilkan dengan nama dan opsi logout. Jika belum login, opsi login dan register ditampilkan.
- Info Card: Pada halaman utama, beberapa card disertakan untuk menampilkan informasi penting seperti NPM, Name, dan Class. Card ini dibuat dinamis agar tampil rapi di berbagai ukuran layar menggunakan Tailwind CSS Grid System.
- Product Display: Produk yang ada ditampilkan dalam grid layout yang responsif. Jika tidak ada produk, gambar dengan ekspresi sedih dan pesan "Belum ada data product" ditampilkan. Jika ada produk, masing-masing produk dimasukkan ke dalam card dengan detail produk dan gambar yang diambil dari template card_product.html.
- Button "Add New Product": Tombol untuk menambah produk baru ditempatkan di bagian kanan atas dan diberi gaya interaktif dengan efek hover dan transformasi menggunakan Tailwind.

Template base.html:
- Global Style: File base.html diubah untuk menggunakan Tailwind CSS secara keseluruhan. Saya memuat file CSS global tambahan untuk elemen styling yang lebih spesifik. Hal ini juga termasuk optimasi agar layout responsif dan mudah digunakan di berbagai perangkat.
- Consistent Layout: Blok konten di dalam {% block content %} memastikan setiap halaman yang mewarisi base.html memiliki layout yang konsisten.

Navbar Dinamis:
- Desktop vs Mobile: Navbar diatur untuk tampil berbeda di perangkat desktop dan mobile. Pada layar kecil, sebuah button akan muncul yang memicu menu dropdown ketika di-klik. Hal ini memastikan pengalaman pengguna yang lancar pada perangkat dengan ukuran layar berbeda.
- Conditional Rendering: Untuk pengguna yang sudah login, navbar akan menampilkan opsi logout dan pesan sambutan, sedangkan pengguna yang belum login akan diberikan opsi login dan register.

# TUGAS INDIVIDU 4
1. Apa perbedaan antara HttpResponseRedirect() dan redirect()

Di Django, baik HttpResponseRedirect() maupun redirect() digunakan untuk mengarahkan pengguna ke URL lain, tetapi ada perbedaan penting antara keduanya.

HttpResponseRedirect(): Kelas ini mengembalikan respons HTTP 302 dengan URL yang diberikan secara langsung. Anda harus menyertakan URL secara eksplisit, baik sebagai string lengkap atau relatif. Cocok untuk redirect sederhana ketika URL tujuan sudah jelas.

redirect(): Fungsi ini lebih fleksibel dan dapat menangani berbagai jenis argumen, seperti string URL, nama view, atau objek model. Misalnya, Anda bisa menggunakan redirect('view_name') untuk mengarahkan ke view tertentu. Django secara otomatis mengonversi argumen menjadi URL yang sesuai, sehingga lebih praktis untuk digunakan dalam berbagai konteks.

Kesimpulan: Gunakan HttpResponseRedirect() untuk redirect sederhana dengan URL yang pasti, dan redirect() untuk kemudahan dan fleksibilitas dalam pengalihan ke berbagai jenis URL.

2. Jelaskan cara kerja penghubungan model Product dengan User!

- Definisikan Model Product
```html
import uuid
from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
```
Penjelasan Struktur
user: Merupakan field dengan tipe ForeignKey yang menghubungkan model Product dengan model User. Setiap produk terkait dengan satu pengguna sebagai pemilik.
on_delete=models.CASCADE: Menentukan bahwa jika pengguna dihapus, semua produk yang terkait dengan pengguna tersebut juga akan dihapus otomatis.

- Proses Membuat Produk
```html
def create_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        product = form.save(commit=False)
        product.user = request.user 
        product.save()
        return redirect('main:show_main')
```
Langkah-langkah:
- Inisialisasi Formulir: Formulir ProductForm diisi dengan data dari request.POST.
- Validasi: Memeriksa kevalidan formulir. Jika valid dan metode permintaan adalah POST, data akan diproses.
- Mengaitkan Pengguna: Produk yang dibuat dihubungkan dengan pengguna yang sedang login melalui request.user.
- Menyimpan Produk: Produk disimpan ke dalam database, membangun relasi permanen antara produk dan pengguna.

Mengakses Produk oleh Pengguna

Setelah produk dibuat, kita dapat mengakses semua produk yang dimiliki pengguna dengan query berikut:
```html
products = Product.objects.filter(user=request.user)
```
Query ini mengembalikan semua objek Product yang terkait dengan pengguna yang sedang login.

- Kesimpulan
Penghubungan antara model Product dan User memungkinkan pelacakan kepemilikan produk dalam aplikasi. Dengan menggunakan ForeignKey, data produk dapat dikelola berdasarkan pengguna, menjaga integritas data, dan memastikan setiap produk terhubung dengan pemiliknya.

3. Apa perbedaan antara authentication dan authorization, apakah yang dilakukan saat pengguna login? Jelaskan bagaimana Django mengimplementasikan kedua konsep tersebut.

Perbedaan Antara Authentication dan Authorization

- Authentication
Merupakan mekanisme verifikasi terkait sapakah yang ingin mengakses web page, apakah user tersebut terdaftar pada sistem? Authentication penting karena semacam step awal dari user untuk dapat mengakses web page yang menerapkan authorization, apabila user tidak terdaftar pada sistem maka user tidak akan dapat mengakses web page tersebut. Hal ini penting untuk segi keamanan web juga untuk memastikan hanya user yang terdaftar yang dapat mengakses

- Authorization
Merupakan mekanisme verifikasi apakah user yang telah terautentikasi dapat mengakses suatu web, fitur, resources, etc. Authorization penting karena digunakan untuk mengelola dan membatasi apa saja hal-hal yang dapat dilakukan dan tidak dapat dilakukan oleh seorang user. Hal ini penting untuk pengelolaan pengguna juga agar tidak ada user yang dapat mengakses/mengubah suatu hal yang seharusnya hanya dapat diakses oleh beberapa user

- Saat pengguna login, proses yang dilakukan mencakup:

Authentication: Memverifikasi kredensial pengguna (misalnya, nama pengguna dan kata sandi).

Authorization: Setelah berhasil login, sistem akan menentukan akses dan hak pengguna berdasarkan peran atau izin yang telah ditentukan.

- Implementasi Authentication dan Authorization di Django

Authentication di Django:
Django menyediakan sistem autentikasi built-in yang memungkinkan pengguna untuk login menggunakan username dan password dapat menggunakan model untuk menyimpan informasi pengguna dan menggunakan view untuk menangani proses login. Django juga menyediakan middleware yang menangani sesi pengguna, sehingga setelah login, pengguna dapat diidentifikasi di seluruh aplikasi.

Authorization di Django:
Django memungkinkan untuk menetapkan izin (permissions) dan grup (groups) untuk pengguna, yang dapat digunakan untuk mengontrol akses ke berbagai bagian aplikasi. Dapat menggunakan dekorator seperti @login_required dan @permission_required untuk melindungi view tertentu, memastikan hanya pengguna yang terautentikasi dan memiliki izin yang tepat yang dapat mengaksesnya.

4. Bagaimana Django mengingat pengguna yang telah login? Jelaskan kegunaan lain dari cookies dan apakah semua cookies aman digunakan?

Di Django, pengguna yang telah login diingat melalui mekanisme session yang menggunakan cookies. Ketika pengguna berhasil login, Django membuat session ID yang unik dan menyimpannya dalam cookie di browser pengguna. Session ini terkait dengan data pengguna yang disimpan di server. Jadi, setiap kali pengguna melakukan request, session ID dari cookie ini dikirimkan kembali ke server sehingga Django bisa mengidentifikasi pengguna yang sedang aktif.

Kegunaan Lain dari Cookies
Selain mengelola sesi pengguna seperti di atas, cookies memiliki beberapa kegunaan lain:
- Menyimpan Preferensi Pengguna: Cookies dapat digunakan untuk menyimpan informasi seperti bahasa yang dipilih pengguna, tema yang dipilih (dark mode/light mode), dan preferensi lainnya sehingga pengguna tidak perlu memilih ulang pada kunjungan berikutnya.
- Personalisasi Konten: Cookies memungkinkan situs web mempersonalisasi konten untuk pengguna, seperti rekomendasi produk berdasarkan kunjungan sebelumnya.
- Tracking dan Analytics: Cookies digunakan oleh situs web untuk melacak perilaku pengguna, misalnya berapa kali pengguna mengunjungi halaman tertentu, yang berguna untuk keperluan analitik.
- Iklan yang Ditargetkan: Cookies memungkinkan platform iklan menampilkan iklan yang relevan kepada pengguna berdasarkan aktivitas penjelajahan mereka di berbagai situs web.

Sebenarnya cookie tidak berbahaya karena cookie hanyalah sebuah data dan bersifat pasif. Hanya saja, walaupun cookie bersifat pasif (hanya merupakan data dan tidak bisa mengakses data, membaca data, maupun mengganti data yang ada di sistem), penggunaan cookies dalam pengembangan web tetap memiliki sejumlah risiko potensial yang perlu diwaspadai. Perlu dicatat bahwa yang berbahaya bukan cookie, melainkan bagaimana cara cookies digunakan dalam konteks aplikasi web yang ternyata dapat disalahgunakan. Dalam penggunaan cookies, harus waspada terkait CSRF, XSS, Cookie theft, dan lain-lain. Oleh karena itu, sebaiknya tidak menyimpan data yang tergolong sensitif di cookies.

5. Jelaskan bagaimana cara kamu mengimplementasikan checklist di atas secara step-by-step (bukan hanya sekadar mengikuti tutorial).

- Mengimplementasikan fungsi registrasi, login, dan logout untuk memungkinkan pengguna untuk mengakses aplikasi sebelumnya dengan lancar.
- Tambahkan kode berikut ke main/views.py
```html
def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
   if request.method == 'POST':
      form = AuthenticationForm(data=request.POST)

      if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response

   else:
      form = AuthenticationForm(request)
   context = {'form': form}
   return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response
```
- response.setcookie('last_login', str(datetime.datetime.now())) digunakan untuk menyimpan waktu terakhir user yang bersangkutan login pada cookie
- Tambahkan 'last_login': request.COOKIES['last_login'], pada context di views.py untuk mengakses cookie last_login
- Tambahkan @login_required(login_url='/login') di atas function show_main pada views.py untuk memastikan hanya logged in user yang bisa akses
- Tambahkan potongan kode berikut pada urls.py untuk handle routing:
```html
path('register/', register, name='register'),
path('login/', login_user, name='login'),
path('logout/', logout_user, name='logout'),
```
- Buat template yang akan digunakan untuk masing-masing routing dari views.py (klik untuk mengakses):
[register.html](main/templates/register.html)
[main.html](main/templates/main.html)
[login.html](main/templates/login.html)
- Membuat dua akun pengguna dengan masing-masing tiga dummy data menggunakan model yang telah dibuat pada aplikasi sebelumnya untuk setiap akun di lokal.
- Buka localhost:8000 dan register untuk 2 username dengan username yang berbeda dan password
- Login ntuk kedua user tersebut, kemudian buat 3 product/item baru dengan klik tombol Add New Product dan isi seluruh detail product yang diinginkan
- Setelah selesai coba cek apakah product yang ditambahkan sudah ada di tabel
- Apabila sudah benar, seharusnya setiap user memiliki tabel dengan isi product yang berbeda-beda
-  Menghubungkan model Item dengan User.
- Tambahkan user = models.ForeignKey(User, on_delete=models.CASCADE) pada class Product di models.py untuk initiate Many to One relationship (karena menggunakan ForeignKey) pada User dengan Product/Item.
- Ubah views.py pada bagian:
```html
def create_product(request):
form = ProductForm(request.POST or None)

if form.is_valid() and request.method == "POST":
    product = form.save(commit=False)
    product.user = request.user
    product.save()
    return redirect('main:show_main')
```
- Tambahkan products = Product.objects.filter(user=request.user) dan ubah context untuk key 'name'
```html
def show_main(request):
products = Product.objects.filter(user=request.user)

context = {
    'name': request.user.username,
    ...
}
```
- Lakukan migration untuk menyimpan perubahan
- Menampilkan detail informasi pengguna yang sedang logged in seperti username dan menerapkan cookies seperti last login pada halaman utama aplikasi.
- Untuk menampilkan username dapat menggunakan potongan kode berikut pada main.html:
```html
<p>{{ name }}</p>
```
- Untuk menampilkan data last login user dapat memanfaatkan Cookies dengan menggunakan potongan kode berikut pada main.html:
```html
<h5>Sesi terakhir login: {{ last_login }}</h5>
```
- Untuk mengimplementasikan cookiesnya sebagai berikut:
- response.set_cookie('last_login', str(datetime.datetime.now())) pada function login_user di views.py untuk set cookie kapan user login terakhir kali
- response.delete_cookie('last_login') pada function logout_user di views.py untuk menghapus cookie
- 'last_login': request.COOKIES['last_login'], pada context function show_main di views.py

# TUGAS INDIVIDU 3

1. Jelaskan mengapa kita memerlukan data delivery dalam pengimplementasian sebuah platform?

Data delivery sangat penting dalam pengimplementasian sebuah platform karena berperan dalam memastikan ketersediaan layanan. Tanpa mekanisme pengiriman data yang tepat, pengguna mungkin mengalami keterlambatan atau bahkan kehilangan akses terhadap informasi yang diperlukan. Ini bisa berdampak negatif pada pengalaman pengguna dan kinerja platform secara keseluruhan. Selain itu, data delivery yang efisien memungkinkan integrasi antara berbagai sistem dan aplikasi di dalam platform, memastikan bahwa data dapat dikirim dan diterima tanpa hambatan. Hal ini juga mendukung konsistensi data, yang penting untuk menjaga integritas informasi antar sistem. 

Di samping itu, platform yang memiliki data delivery yang baik lebih mampu beradaptasi dengan pertumbuhan pengguna dan peningkatan volume data, sehingga memastikan skalabilitas yang dibutuhkan seiring perkembangan platform. Mekanisme ini juga memungkinkan keamanan data yang lebih kuat dengan memastikan bahwa data hanya diakses oleh pihak yang berwenang, melindungi informasi sensitif dari potensi ancaman.

2. Menurutmu, mana yang lebih baik antara XML dan JSON? Mengapa JSON lebih populer dibandingkan XML?

Menurut saya, JSON secara umum lebih baik untuk kebanyakan kasus penggunaan modern, terutama dalam pengembangan aplikasi web dan komunikasi data yang membutuhkan kecepatan dan efisiensi. JSON lebih ringan, lebih mudah dibaca, dan lebih cepat diproses dibandingkan XML. Selain itu, JSON memiliki integrasi yang sangat baik dengan bahasa pemrograman seperti JavaScript, yang membuatnya lebih populer dalam pengembangan aplikasi berbasis web.

Namun, jika memerlukan validasi skema yang kuat atau bekerja dengan data yang kompleks dan terstruktur (misalnya, dengan metadata atau atribut), XML bisa menjadi pilihan yang lebih tepat karena dukungan untuk skema yang lebih formal.

Secara keseluruhan, untuk penggunaan umum yang melibatkan pertukaran data sederhana, JSON biasanya merupakan pilihan yang lebih baik.

JSON lebih populer dibandingkan XML karena :
- Tingkat simplicity dan readability yang tinggi karena syntax dan indentasinya yang ringkas
- Memiliki banyak method yang dapat mempercepat proses penyusunan program (contoh: JSON.parse() untuk mengubah JSON string menjadi Object dengan atribut-atributnya)
- Dapat merepresentasikan data dengan ukuran file yang kecil karena syntaxnya ringkas (seperti tidak menggunakan tag, etc.)
- Dapat melakukan transfer/pertukaran data dengan sangat cepat (tidak perlu banyak parse karena syntaxnya juga singkat)
- Sangat compatible dengan berbagai teknologi web, seperti JavaScript dan lain-lain.
- Mendukung tipe data native, seperti numbers, booleans, null, etc.

3. Jelaskan fungsi dari method is_valid() pada form Django dan mengapa kita membutuhkan method tersebut?

Method is_valid() pada form Django digunakan untuk memeriksa apakah data yang dimasukkan ke dalam form memenuhi semua validasi yang telah ditentukan, baik dari validasi bawaan Django maupun validasi custom. Method ini akan mengembalikan nilai True jika data valid, dan False jika tidak.

Kita membutuhkan method ini untuk memastikan bahwa data yang diolah sudah benar sebelum disimpan ke database atau diproses lebih lanjut, sehingga mencegah kesalahan atau data yang tidak sesuai.

4. Mengapa kita membutuhkan csrf_token saat membuat form di Django? Apa yang dapat terjadi jika kita tidak menambahkan csrf_token pada form Django? Bagaimana hal tersebut dapat dimanfaatkan oleh penyerang?

Dalam Django, kita membutuhkan csrf_token untuk melindungi aplikasi dari serangan Cross-Site Request Forgery (CSRF). Serangan ini terjadi ketika penyerang mencoba mengirimkan permintaan berbahaya atas nama pengguna tanpa izin mereka. Misalnya, jika pengguna sedang login ke suatu aplikasi, penyerang bisa memanfaatkan celah ini untuk melakukan aksi seperti mengubah data atau menjalankan transaksi tanpa sepengetahuan pengguna.

Dengan menambahkan csrf_token pada form, Django memastikan bahwa setiap permintaan yang dikirim benar-benar berasal dari sumber yang sah (form asli di situs), bukan dari halaman eksternal yang dibuat oleh penyerang. Tanpa csrf_token, aplikasi rentan terhadap serangan ini, yang bisa berdampak pada keamanan dan integritas data.

5. Jelaskan bagaimana cara kamu mengimplementasikan checklist di atas secara step-by-step (bukan hanya sekadar mengikuti tutorial).

- Membuat base.html pada root/templates dan mengisinya dengan:
```html
{% load static %}
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    {% block meta %} {% endblock meta %}
  </head>

  <body>
    {% block content %} {% endblock content %}
  </body>
</html>
```
- Membuat forms.py pada main dan mengisinya dengan:
```html
from django.forms import ModelForm
from main.models import Product

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "price"]
```
- Ubah function show_main pada views.py menjadi sebagai berikut:
```html
def show_main(request):
    products = Product.objects.all()

    context = {
        'name': 'Sarah Saphira Setiawan',
        'npm' : '2306240093',
        'class': 'PBP A',
        'products': products
    }

    return render(request, "main.html", context)
```
- Buat create_product.html pada main/templates/ dan isi sebagai berikut:
```html
{% extends 'base.html' %} 
{% block content %}
<h1>Add New Product</h1>

<form method="POST">
  {% csrf_token %}
  <table>
    {{ form.as_table }}
    <tr>
      <td></td>
      <td>
        <input type="submit" value="Add Product" />
      </td>
    </tr>
  </table>
</form>
```
- Tambahkan 5 fungsi views untuk melihat objek yang sudah ditambahkan dalam format HTML, XML, JSON, XML by ID, dan JSON by ID.

- create_product untuk menerima input user, dapat diakses ketika user klik button "Add New Product"
```html
def create_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_product.html", context)
```
- show_xml untuk menampilkan representasi seluruh products dalam format XML
```html
def show_xml(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")
```
- show_json untuk menampilkan representasi seluruh products dalam format JSON,
```html
def show_json(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
```
- show_xml_by_id untuk menampilkan representasi product dengan id yang diinginkan dalam format XML
```html
def show_xml_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")
```
- show_json_by_id untuk menampilkan representasi product dengan id yang diinginkan dalam format JSON
```html
def show_json_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
```
- Membuat routing URL untuk masing-masing views

- Isi urls.py dengan:
```html
from django.urls import path
from main.views import show_main, create_product, show_xml, show_json, show_xml_by_id, show_json_by_id

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('create-product', create_product, name='create_product'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
]
```
- urlpatterns digunakan agar function-function yang telah dicantumkan pada views.py dapat diakses dengan url yang diinginkan.

6. Mengakses keempat URL di poin 2 menggunakan Postman, membuat screenshot dari hasil akses URL pada Postman

- XML: (url)/xml: Untuk menampilkan representasi seluruh products dalam format XML
![](https://github.com/sarahsaphira/cookies-store/blob/fa5ccb3d9a3fbbc8417ffb8a28bca29d71c718f4/xml.png)

- JSON: (url)/json: Untuk menampilkan representasi seluruh products dalam format JSON
![](https://github.com/sarahsaphira/cookies-store/blob/fa5ccb3d9a3fbbc8417ffb8a28bca29d71c718f4/json.png)

- XML by ID: (url)/xml/(desired_id): Untuk menampilkan representasi product dengan id yang diinginkan dalam format XML
![](https://github.com/sarahsaphira/cookies-store/blob/fa5ccb3d9a3fbbc8417ffb8a28bca29d71c718f4/XMLbyID.png)

- JSON by ID: (url)/xml/(desired_id): Untuk menampilkan representasi product dengan id yang diinginkan dalam format JSON
![](https://github.com/sarahsaphira/cookies-store/blob/fa5ccb3d9a3fbbc8417ffb8a28bca29d71c718f4/JSONbyID.png)

# TUGAS INDIVIDU 2
1. Jelaskan bagaimana cara kamu mengimplementasikan checklist di atas secara step-by-step (bukan hanya sekadar mengikuti tutorial)

Cara Pengerjaan Checklist
- Membuat sebuah proyek Django baru.
- Membuat direktori baru bernama cookies-store yang akan dijadikan local directory
- Membuat repository github baru bernama cookies-store
- Membuat file README.md dan mengeditnya melalui VSCODE
- Membuka CMD pada directory cookies-store dan menjalankan git init, git branch -M main, git remote add origin https://github.com/sarahsaphira/cookies-store.git, dan git push -u origin main untuk membuat main branch dengan nama main, menghubungkan local directory/repository dengan repository github, dan push/update semua perubahan ke github
- Menjalankan python3 -m venv env untuk membuat virtual environment untuk directory agar dapat maintain versi-versi django dan lain sebagainya yang dipakai di device
- Menjalankan source env/bin/activate untuk mengaktifkan virtual environment
- Membuat file baru bernama requirements.txt dan mengisinya dengan hal-hal yang ingin diinstall agar tidak terlalu banyak menjalankan command pip install, saya mengisinya dengan:
- Menjalankan pip install -r requirements.txt untuk install hal-hal yang telah ditambahkan pada requirements.txt tadi
- Menjalankan django-admin startproject cookies_store .
- Membuka file settings.py dan ubah ALLOWED_HOSTS = [] menjadi ALLOWED_HOSTS = ["localhost", "127.0.0.1"] karena akan diperlukan untuk proses deployment
- Membuat file baru bernama .gitignore untuk memberikan informasi mengenai berkas yang perubahannya tidak perlu ditrack oleh Git,
- Membuat aplikasi dengan nama main pada proyek tersebut.
- Masih pada CMD yang sama, jalankan python3 manage.py startapp main untuk membuat django app baru bernama main pada django project bernama cookies_store
- Membuka file settings.py dan tambahkan 'main' pada variabel INSTALLED_APPS
- Membuka directory main dan buat directory baru bernama templates untuk menyimpan file main.html yang akan digunakan karena django menggunakan Model-View-Template (MVT)
- Membuat file baru bernama main.html pada directory templates dan mengisinya dengan konten-konten yang diperlukan. 
- Melakukan routing pada proyek agar dapat menjalankan aplikasi main.
- Membuka file urls.py pada directory cookies_store
- Menambahkan from django.urls import path, include
- Mengubah urlpatterns menjadi:
```html
urlpatterns = [
    path('', include('main.urls')),
]
```

- Membuat model pada aplikasi main dengan nama Item dan memiliki atribut wajib sebagai berikut.
name sebagai nama item dengan tipe CharField.
price sebagai harga item dengan tipe IntegerField.
description sebagai deskripsi item dengan tipe TextField.

- membuka models.py dan mengisinya dengan attributes/fields yang diperlukan. Pada kasus ini, saya menggunakan 3 attributes, yakni name (CharField), price (IntegerField), description (TextField). Isi file models.py adalah sebagai berikut:
```html
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
```

- Membuka views.py dan menambahkan potongan kode di bawah ini untuk menghubungkan Views dan Templates. Sehingga, isi views.py sebagai berikut:
```html
from django.shortcuts import render

def show_main(request):
    context = {
        'npm' : '2306240093',
        'name': 'Sarah Saphira Setiawan',
        'class': 'PBP A'
    }

    return render(request, "main.html", context)

- ubah urlpatterns menjadi seperti ini:
urlpatterns = [
    path('', show_main, name='show_main'), 
]
```

- Menjalankan git push origin main, git add . , git commit -m "message", dan git push -u origin main untuk update github repository agar sesuai dengan local repository

2. Buatlah bagan yang berisi request client ke web aplikasi berbasis Django beserta responnya dan jelaskan pada bagan tersebut kaitan antara urls.py, views.py, models.py, dan berkas html.
![](https://github.com/sarahsaphira/cookies-store/blob/1b0f33067c635ff55e09f6e077944304a335bbb5/BaganNomor2.png)

Client mengirim request ke Internet -> forward ke Python/Django -> forward ke urls.py -> forward ke views.py untuk memproses url -> read/write data dari/ke models.py dan database -> input/display data dari/ke templates -> return html file yang telah dimerge dengan value-value yang diinginkan -> proses ke internet -> display ke client's device

3. Jelaskan fungsi git dalam pengembangan perangkat lunak!

Git berfungsi sebagai alat penting dalam pengembangan perangkat lunak karena membantu tim pengembang mengelola perubahan pada kode. Dengan Git, setiap perubahan yang dilakukan dicatat, sehingga pengembang bisa melihat versi-versi sebelumnya, siapa yang melakukan perubahan, dan alasan perubahan tersebut.

Git juga memudahkan kerja sama tim. Beberapa orang bisa bekerja di proyek yang sama tanpa perlu khawatir akan mengganggu pekerjaan satu sama lain. Mereka bisa membuat cabang (branch) dari kode utama untuk mengembangkan fitur baru atau memperbaiki masalah, lalu menggabungkannya kembali setelah selesai.

Selain itu, Git memungkinkan kita untuk kembali ke versi kode yang stabil jika terjadi kesalahan. Ini memberikan rasa aman karena kita selalu bisa memulihkan kode yang sudah bekerja dengan baik. Jika ada konflik ketika beberapa orang mengubah bagian kode yang sama, Git juga membantu menyelesaikan masalah ini.

4. Menurut Anda, dari semua framework yang ada, mengapa framework Django dijadikan permulaan pembelajaran pengembangan perangkat lunak?

Django sering dipilih sebagai framework pertama dalam pembelajaran pengembangan perangkat lunak karena memiliki beberapa keunggulan yang membuatnya cocok untuk pemula. Pertama, Django sudah dilengkapi dengan banyak fitur bawaan, seperti autentikasi pengguna, manajemen database, dan URL routing, sehingga kita tidak perlu membangun semuanya dari nol. Ini membantu pengembang baru untuk lebih fokus pada logika aplikasi daripada hal-hal teknis yang rumit.

Selain itu, Django mengikuti prinsip "batteries included", yang berarti banyak kebutuhan pengembangan umum sudah tersedia dan siap pakai. Ini membuat proses belajar lebih mudah karena pengembang tidak harus mencari atau mengatur banyak alat tambahan.

Django juga mengedepankan praktik pengembangan yang baik, seperti pembagian tugas antara bagian yang mengatur logika (views), data (models), dan tampilan (templates) melalui arsitektur Model-View-Template (MVT). Dengan pendekatan ini, pengembang belajar cara mengorganisasi kode dengan baik dari awal.

5. Mengapa model pada Django disebut sebagai ORM?

Model dalam Django disebut ORM (Object-Relational Mapping) karena memungkinkan kita bekerja dengan data di database menggunakan objek Python, tanpa harus menulis perintah SQL secara langsung. Django ORM menghubungkan objek Python dengan tabel di database relasional.

Jadi, saat kita membuat model di Django, misalnya model Product, Django akan mengubahnya menjadi tabel product di database, dan setiap atribut dari model tersebut akan menjadi kolom di tabel. ORM mempermudah kita untuk mengambil, menyimpan, atau mengubah data hanya dengan menggunakan metode pada objek Python, tanpa perlu berurusan dengan query SQL yang kompleks.

ORM juga memastikan agar struktur kode dan database tetap konsisten. Jika ada perubahan pada model, Django bisa otomatis menyesuaikan perubahan tersebut ke dalam database melalui fitur migrasi. Ini membantu kita menghindari pengelolaan database secara manual, membuat pengembangan lebih cepat dan mudah.

Intinya, Django menggunakan ORM untuk memetakan objek Python ke tabel database, sehingga kita bisa bekerja dengan database secara lebih sederhana dan efisien.